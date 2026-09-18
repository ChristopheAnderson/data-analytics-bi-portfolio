"""
Projet 1 : Logistique Portuaire & Chaîne d'Approvisionnement Multimodale (Cible AGL)
Moteur de données et calcul de KPIs opérationnels pour terminaux à conteneurs
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_port_operations_data(n_vessels=180, seed=42):
    """Génère un jeu de données réaliste d'escales navires et mouvements de conteneurs."""
    np.random.seed(seed)
    
    shipping_lines = ['Maersk', 'MSC', 'CMA CGM', 'Hapag-Lloyd', 'COSCO', 'Grimaldi']
    vessel_types = ['Porte-conteneurs Feeder', 'Porte-conteneurs Panamax', 'Porte-conteneurs Post-Panamax', 'Roulier / Ro-Ro']
    terminals = ['Terminal Conteneurs Sud', 'Terminal Conteneurs Nord', 'Quai Polyvalent']
    berths = ['Poste 1', 'Poste 2', 'Poste 3', 'Poste 4', 'Poste 5']
    
    start_date = datetime(2026, 1, 1)
    
    records = []
    for i in range(n_vessels):
        arrival_delta = timedelta(days=float(np.random.exponential(scale=1.2) * (i + 1) * 0.4),
                                  hours=float(np.random.randint(0, 24)))
        arrival_time = start_date + arrival_delta
        
        # Temps d'attente au mouillage (rade) en heures
        waiting_hours = float(np.clip(np.random.exponential(scale=14.0) + (np.random.choice([0, 24, 48], p=[0.7, 0.2, 0.1])), 2.0, 96.0))
        berthing_time = arrival_time + timedelta(hours=waiting_hours)
        
        vtype = np.random.choice(vessel_types, p=[0.4, 0.35, 0.15, 0.1])
        sline = np.random.choice(shipping_lines)
        
        # Volumes EVP (Équivalent Vingt Pieds)
        if 'Post-Panamax' in vtype:
            teu_import = int(np.random.normal(1800, 300))
            teu_export = int(np.random.normal(1200, 250))
            cranes_assigned = np.random.choice([3, 4], p=[0.4, 0.6])
        elif 'Panamax' in vtype:
            teu_import = int(np.random.normal(1100, 200))
            teu_export = int(np.random.normal(850, 180))
            cranes_assigned = np.random.choice([2, 3], p=[0.5, 0.5])
        elif 'Feeder' in vtype:
            teu_import = int(np.random.normal(450, 120))
            teu_export = int(np.random.normal(380, 100))
            cranes_assigned = np.random.choice([1, 2], p=[0.6, 0.4])
        else: # Ro-Ro
            teu_import = int(np.random.normal(250, 80))
            teu_export = int(np.random.normal(200, 70))
            cranes_assigned = 1
            
        total_teu = max(teu_import + teu_export, 100)
        
        # Cadence moyenne de manutention par grue (EVP/heure)
        crane_rate = float(np.clip(np.random.normal(24.5, 3.2), 15.0, 35.0))
        effective_rate = crane_rate * cranes_assigned
        
        operation_hours = float(np.clip(total_teu / effective_rate, 4.0, 80.0))
        departure_time = berthing_time + timedelta(hours=operation_hours)
        
        # Temps total d'escale (Turnaround Time)
        total_turnaround_hours = waiting_hours + operation_hours
        
        records.append({
            'vessel_id': f"VSL-2026-{i+1:04d}",
            'vessel_name': f"M/V {sline} {['Atlantic', 'Breeze', 'Voyager', 'Pioneer', 'Horizon', 'Express'][i % 6]}",
            'shipping_line': sline,
            'vessel_type': vtype,
            'arrival_time': arrival_time,
            'berthing_time': berthing_time,
            'departure_time': departure_time,
            'waiting_hours_anchorage': round(waiting_hours, 1),
            'operation_hours_berth': round(operation_hours, 1),
            'turnaround_time_hours': round(total_turnaround_hours, 1),
            'teu_import': max(teu_import, 10),
            'teu_export': max(teu_export, 10),
            'total_teu': total_teu,
            'cranes_assigned': cranes_assigned,
            'crane_productivity_teu_hr': round(crane_rate, 1),
            'terminal': np.random.choice(terminals),
            'berth': np.random.choice(berths),
            'status': 'Terminé' if i < n_vessels - 5 else 'À quai',
            'congestion_alert': waiting_hours > 24.0
        })
        
    df = pd.DataFrame(records)
    return df

def compute_port_kpis(df):
    """Calcule la synthèse décisionnelle des indicateurs portuaires."""
    total_teu = df['total_teu'].sum()
    avg_waiting = df['waiting_hours_anchorage'].mean()
    avg_berth_time = df['operation_hours_berth'].mean()
    avg_turnaround = df['turnaround_time_hours'].mean()
    avg_crane_prod = df['crane_productivity_teu_hr'].mean()
    congestion_rate = (df['congestion_alert'].sum() / len(df)) * 100
    
    return {
        'total_vessels': len(df),
        'total_teu_handled': int(total_teu),
        'avg_anchorage_wait_hours': round(avg_waiting, 1),
        'avg_berth_op_hours': round(avg_berth_time, 1),
        'avg_turnaround_time_hours': round(avg_turnaround, 1),
        'avg_crane_productivity': round(avg_crane_prod, 1),
        'congestion_frequency_pct': round(congestion_rate, 1)
    }

if __name__ == "__main__":
    data = generate_port_operations_data(50)
    kpis = compute_port_kpis(data)
    print("Moteur de données logistiques opérationnel.")
    print("KPIs calculés :", kpis)
