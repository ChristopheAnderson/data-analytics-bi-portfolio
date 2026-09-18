"""
Projet 4 : Modélisation Prévisionnelle & Dashboard Décisionnel ODD (Cible Expertise France / ONU)
Moteur de prévision sur séries temporelles socio-économiques & suivi d'indicateurs de gouvernance
"""

import numpy as np
import pandas as pd
from datetime import datetime

def generate_development_indicators_series(n_months=48, seed=2026):
    """
    Génère une série temporelle mensuelle (2022 à 2025) d'indicateurs de développement socio-économique
    (ex: Taux d'électrification rurale, indice d'inclusion financière mobile, émissions CO2 évitées).
    """
    np.random.seed(seed)
    
    dates = pd.date_range(start="2022-01-01", periods=n_months, freq="MS")
    t = np.arange(n_months)
    
    # Indicateur 1 : Taux d'électrification rurale (%) - Tendance haussière + saisonnalité agricole
    trend_electrif = 22.0 + 0.45 * t
    season_electrif = 1.8 * np.sin(2 * np.pi * t / 12)
    noise_electrif = np.random.normal(0, 0.6, n_months)
    rural_electrification_pct = np.clip(trend_electrif + season_electrif + noise_electrif, 15.0, 70.0)
    
    # Indicateur 2 : Inclusion financière digitale / Mobile Money (% adultes)
    trend_fintech = 35.0 + 0.65 * t
    noise_fintech = np.random.normal(0, 0.9, n_months)
    mobile_money_penetration_pct = np.clip(trend_fintech + noise_fintech, 20.0, 85.0)
    
    # Indicateur 3 : Décaissements de projets d'appui technique (k€)
    budget_disbursed_k_eur = 180.0 + 3.2 * t + 25.0 * np.cos(2 * np.pi * t / 12) + np.random.normal(0, 12, n_months)
    
    df = pd.DataFrame({
        'date': dates,
        'rural_electrification_pct': np.round(rural_electrification_pct, 2),
        'mobile_money_penetration_pct': np.round(mobile_money_penetration_pct, 2),
        'budget_disbursed_k_eur': np.round(budget_disbursed_k_eur, 1)
    })
    
    return df

def forecast_time_series(df, target_col='rural_electrification_pct', horizon_months=12):
    """
    Modèle de régression linéaire prédictive avec décomposition de tendance et saisonnalité
    pour projection à l'horizon souhaité avec intervalle de confiance à 95%.
    """
    y = df[target_col].values
    n = len(y)
    x = np.arange(n)
    
    # Ajustement modèle linéaire
    poly_coefs = np.polyfit(x, y, deg=1)
    fitted_trend = np.polyval(poly_coefs, x)
    residuals = y - fitted_trend
    residual_std = np.std(residuals)
    
    # Prévisions futures
    future_x = np.arange(n, n + horizon_months)
    last_date = df['date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=horizon_months, freq="MS")
    
    # Estimation de la saisonnalité moyenne sur les 12 mois
    monthly_seasonality = np.zeros(12)
    for i in range(12):
        month_indices = [idx for idx in range(n) if df['date'].iloc[idx].month == (i + 1)]
        if month_indices:
            monthly_seasonality[i] = np.mean(residuals[month_indices])
            
    future_seasonality = np.array([monthly_seasonality[(d.month - 1)] for d in future_dates])
    future_y_pred = np.polyval(poly_coefs, future_x) + future_seasonality
    
    # Intervalle de confiance 95% (+/- 1.96 * sigma)
    ci_upper = future_y_pred + 1.96 * residual_std
    ci_lower = future_y_pred - 1.96 * residual_std
    
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'forecast': np.round(future_y_pred, 2),
        'lower_bound_95': np.round(ci_lower, 2),
        'upper_bound_95': np.round(ci_upper, 2)
    })
    
    # Métriques de performance historique
    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals**2))
    mape = np.mean(np.abs(residuals / y)) * 100.0
    
    metrics = {
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'mape_pct': round(mape, 2),
        'slope_annual_gain': round(poly_coefs[0] * 12.0, 2)
    }
    
    return forecast_df, metrics

if __name__ == '__main__':
    df = generate_development_indicators_series()
    f_df, m = forecast_time_series(df)
    print("Moteur prévisionnel ODD opérationnel.")
    print("Métriques d'ajustement :", m)
    print("Projections (3 premiers mois) :\n", f_df.head(3))
