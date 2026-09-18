"""
Projet 3 : Pipeline de Données Humanitaires & Audit Qualité KoboToolbox / ODK (Cible IMPACT Initiatives / REACH)
Moteur de détection d'anomalies, journal de nettoyage (Cleaning Log) et évaluation de la vulnérabilité
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_humanitarian_survey_data(n_surveys=350, seed=77):
    """
    Génère un jeu de données simulant une évaluation multisectorielle des besoins (MSNA)
    collectée via KoboToolbox / ODK dans plusieurs départements du Bénin (Alibori, Atacora, Borgou, Zou, Littoral).
    """
    np.random.seed(seed)
    
    departments = ['Alibori', 'Atacora', 'Borgou', 'Zou', 'Littoral']
    enumerators = [f"ENUM_{k:02d}" for k in range(1, 16)]
    
    records = []
    base_time = datetime(2026, 2, 1, 8, 0)
    
    for i in range(n_surveys):
        enum_id = np.random.choice(enumerators)
        dept = np.random.choice(departments, p=[0.25, 0.25, 0.20, 0.15, 0.15])
        
        # Durée de l'enquête en minutes (normale: 35-55 min, suspecte: < 15 min ou > 120 min)
        is_speeding = np.random.rand() < 0.08
        if is_speeding:
            duration_min = float(np.random.uniform(5.0, 14.0))
        else:
            duration_min = float(np.random.normal(42.0, 8.0))
            
        # Composition du ménage
        hh_size = int(np.random.choice([2, 3, 4, 5, 6, 7, 8, 10, 14], p=[0.05, 0.1, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]))
        # Incohérence intentionnelle injectée pour tester l'audit
        has_logic_error = np.random.rand() < 0.06
        if has_logic_error:
            children_under_5 = hh_size + int(np.random.randint(1, 4)) # Incohérent : plus d'enfants <5 ans que de membres totaux
        else:
            children_under_5 = int(np.random.randint(0, min(hh_size, 4)))
            
        # Score de Consommation Alimentaire (FCS - Food Consumption Score : 0 à 112)
        # Seuil PAM/WFP : Pauvre (0-21), Limite (21.5-35), Acceptable (>35)
        fcs_score = float(np.clip(np.random.normal(38.0, 14.0) - (10.0 if dept in ['Alibori', 'Atacora'] else 0), 6.0, 95.0))
        
        # Score d'Indice des Stratégies de Survie (rCSI - reduced Coping Strategy Index : 0 à 56)
        rcsi_score = float(np.clip(np.random.exponential(scale=9.0), 0.0, 48.0))
        
        # Statut de déplacement (Personne déplacée interne PDI / Communauté hôte)
        is_idp = np.random.choice([True, False], p=[0.28, 0.72]) if dept in ['Alibori', 'Atacora'] else False
        
        # Coordonnées géographiques approximatives par département
        coords = {
            'Alibori': (11.4, 2.8),
            'Atacora': (10.6, 1.8),
            'Borgou': (9.3, 2.6),
            'Zou': (7.2, 2.1),
            'Littoral': (6.37, 2.43)
        }
        base_lat, base_lon = coords[dept]
        lat = base_lat + float(np.random.normal(0, 0.15))
        lon = base_lon + float(np.random.normal(0, 0.15))
        
        records.append({
            'survey_uuid': f"uuid:{i+1000:06d}",
            'submission_date': base_time + timedelta(days=int(i/12), hours=int(np.random.randint(0, 10))),
            'enumerator_id': enum_id,
            'department': dept,
            'latitude': round(lat, 5),
            'longitude': round(lon, 5),
            'survey_duration_min': round(duration_min, 1),
            'hh_size': hh_size,
            'children_under_5': children_under_5,
            'fcs_food_consumption': round(fcs_score, 1),
            'rcsi_coping_index': round(rcsi_score, 1),
            'is_idp_displaced': is_idp,
            'water_access_hours_per_day': int(np.random.choice([1, 2, 4, 8, 16, 24], p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.10]))
        })
        
    df = pd.DataFrame(records)
    return df

def audit_humanitarian_data(df):
    """
    Exécute les règles d'audit qualité des données (Quality Checks) :
    1. Détection des durées aberrantes (< 15 min - Speeding survey)
    2. Détection d'incohérence logique (enfants < 5 ans > taille ménage)
    3. Détection d'outliers statistiques sur le score rCSI (IQR 1.5)
    Génère un Cleaning Log complet conforme aux standards IMPACT/REACH.
    """
    cleaning_log = []
    
    # 1. Vérification durée trop courte
    speeders = df[df['survey_duration_min'] < 15.0]
    for _, row in speeders.iterrows():
        cleaning_log.append({
            'uuid': row['survey_uuid'],
            'enumerator_id': row['enumerator_id'],
            'variable': 'survey_duration_min',
            'issue': 'Enquête trop rapide (< 15 min - Speeding flag)',
            'old_value': row['survey_duration_min'],
            'action': 'À vérifier / Flag suspect'
        })
        
    # 2. Vérification cohérence logique démographique
    logic_issues = df[df['children_under_5'] > df['hh_size']]
    for _, row in logic_issues.iterrows():
        cleaning_log.append({
            'uuid': row['survey_uuid'],
            'enumerator_id': row['enumerator_id'],
            'variable': 'children_under_5',
            'issue': 'Enfants <5 ans supérieur à la taille totale du ménage',
            'old_value': f"Enfants: {row['children_under_5']} > Total: {row['hh_size']}",
            'action': 'Correction requise / Recontacter enquêteur'
        })
        
    # 3. Détection d'outliers rCSI
    q75, q25 = np.percentile(df['rcsi_coping_index'], [75, 25])
    iqr = q75 - q25
    upper_bound = q75 + 2.0 * iqr
    outliers_rcsi = df[df['rcsi_coping_index'] > upper_bound]
    for _, row in outliers_rcsi.iterrows():
        cleaning_log.append({
            'uuid': row['survey_uuid'],
            'enumerator_id': row['enumerator_id'],
            'variable': 'rcsi_coping_index',
            'issue': f'Valeur extrême rCSI (> {upper_bound:.1f})',
            'old_value': row['rcsi_coping_index'],
            'action': 'Confirmation terrain nécessaire'
        })
        
    log_df = pd.DataFrame(cleaning_log)
    
    # Score de conformité global (%)
    total_checks = len(df) * 3
    total_anomalies = len(log_df)
    quality_score = max(0.0, min(100.0, 100.0 - (total_anomalies / len(df)) * 100.0))
    
    return {
        'total_surveys': len(df),
        'total_anomalies_detected': total_anomalies,
        'data_quality_score_pct': round(quality_score, 1),
        'speeding_count': len(speeders),
        'logic_errors_count': len(logic_issues),
        'cleaning_log': log_df
    }

if __name__ == '__main__':
    df_raw = generate_humanitarian_survey_data()
    audit_res = audit_humanitarian_data(df_raw)
    print("Audit de données humanitaires terminé.")
    print("Score qualité :", audit_res['data_quality_score_pct'], "%")
    print("Anomalies détectées :", audit_res['total_anomalies_detected'])
