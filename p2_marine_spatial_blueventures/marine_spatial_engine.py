"""
Projet 2 : Analyse Spatiale Marine & Cartographie Côtière (Cible Blue Ventures)
Moteur de traitement géospatial, suivi de l'effort de pêche artisanale & zonage des Aires Marines Protégées (AMP)
"""

import numpy as np
import pandas as pd

def generate_coastal_marine_data(n_samples=250, seed=101):
    """
    Génère un jeu de données géoréférencé sur la zone maritime et côtière du Golfe de Guinée / Bénin.
    Coordonnées centrées sur les côtes ouest-africaines (Lat: 6.10 à 6.45 N, Lon: 2.10 à 2.70 E).
    """
    np.random.seed(seed)
    
    # Coordonnées côtières (Cotonou, Grand-Popo, Ouidah, Sèmè)
    lats = np.random.uniform(6.15, 6.40, n_samples)
    lons = np.random.uniform(2.15, 2.65, n_samples)
    
    # Profondeur bathymétrique (mètres) en fonction de l'éloignement de la côte
    # Plus la latitude est basse (plus au sud en mer), plus c'est profond
    bathymetry = -(6.42 - lats) * 1200 + np.random.normal(0, 8, n_samples)
    bathymetry = np.clip(bathymetry, -120.0, -5.0)
    
    # Types d'engins de pêche artisanale
    gear_types = ['Filet maillant dérivant', 'Senne de plage', 'Ligne à main', 'Nasse artisanale']
    gears = np.random.choice(gear_types, n_samples, p=[0.45, 0.25, 0.20, 0.10])
    
    # Effort de pêche (heures en mer) et captures (kg)
    effort_hours = np.random.gamma(shape=4.0, scale=1.5, size=n_samples)
    # CPUE (Catch Per Unit Effort) : kg par heure
    cpue_base = np.where(bathymetry > -30, 4.2, 7.8) + np.random.normal(0, 1.2, n_samples)
    cpue = np.clip(cpue_base, 0.8, 18.0)
    catch_kg = effort_hours * cpue
    
    # Détection de zones protégées (Aires Marines Protégées - AMP / Aires Communautaires LMMA)
    # Zone protégée fictive A: Lat 6.20 - 6.28, Lon 2.25 - 2.40
    is_protected_zone = (lats >= 6.20) & (lats <= 6.28) & (lons >= 2.25) & (lons <= 2.40)
    
    # Indice d'impact / Pression de pêche (0 à 100)
    fishing_pressure_index = np.clip((effort_hours / 10.0) * 40 + (catch_kg / 100.0) * 60, 5, 98)
    
    # Indice de Santé Écologique Récifale / Mangrove (0 à 10)
    eco_health_index = np.where(is_protected_zone, 8.4 + np.random.normal(0, 0.5, n_samples),
                                4.5 + np.random.normal(0, 1.1, n_samples))
    eco_health_index = np.clip(eco_health_index, 1.0, 10.0)
    
    df = pd.DataFrame({
        'point_id': [f"GEO-BV-{i+1:04d}" for i in range(n_samples)],
        'latitude': np.round(lats, 4),
        'longitude': np.round(lons, 4),
        'bathymetry_m': np.round(bathymetry, 1),
        'gear_type': gears,
        'effort_hours': np.round(effort_hours, 1),
        'cpue_kg_hr': np.round(cpue, 2),
        'total_catch_kg': np.round(catch_kg, 1),
        'fishing_pressure_index': np.round(fishing_pressure_index, 1),
        'eco_health_index': np.round(eco_health_index, 1),
        'in_marine_protected_area': is_protected_zone,
        'site_name': np.random.choice(['Baie de Grand-Popo', 'Zone Côtière Ouidah', 'Plateau Cotonou Ouest', 'Banc Sèmè-Kpodji'], n_samples)
    })
    
    return df

def compute_marine_kpis(df):
    """Calcule la synthèse spatiale et environnementale."""
    total_catch = df['total_catch_kg'].sum()
    avg_cpue = df['cpue_kg_hr'].mean()
    mpa_coverage_pct = (df['in_marine_protected_area'].sum() / len(df)) * 100
    avg_eco_health_protected = df[df['in_marine_protected_area']]['eco_health_index'].mean()
    avg_eco_health_non_protected = df[~df['in_marine_protected_area']]['eco_health_index'].mean()
    
    return {
        'total_catch_tonnes': round(total_catch / 1000.0, 2),
        'avg_cpue_kg_hr': round(avg_cpue, 2),
        'mpa_sample_coverage_pct': round(mpa_coverage_pct, 1),
        'eco_health_in_mpa': round(avg_eco_health_protected, 2),
        'eco_health_outside_mpa': round(avg_eco_health_non_protected, 2),
        'biodiversity_gain_pct': round(((avg_eco_health_protected - avg_eco_health_non_protected) / avg_eco_health_non_protected) * 100, 1)
    }

if __name__ == '__main__':
    data = generate_coastal_marine_data()
    print("Moteur de données spatiales marines opérationnel.")
    print("KPIs marins :", compute_marine_kpis(data))
