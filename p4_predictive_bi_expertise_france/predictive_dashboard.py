"""
Composant Dashboard Streamlit : Modélisation Prévisionnelle & Analyse d'Impact ODD (Cible Expertise France / ONU)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .predictive_engine import generate_development_indicators_series, forecast_time_series

def render_predictive_module():
    st.subheader("📈 P4 : Modélisation Prévisionnelle & Suivi des Indicateurs ODD (Cible Expertise France & ONU)")
    st.markdown(
        """
        **Cas d'Usage Métier :** Modélisation statistique sur séries temporelles, estimation de tendances
        et projections à moyen terme (horizon 12 à 24 mois) avec intervalles de confiance à 95% pour l'aide à la décision stratégique.
        """
    )
    
    df = generate_development_indicators_series()
    
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        indicator_choice = st.selectbox(
            "Sélectionner l'indicateur d'impact ODD :",
            options=[
                ('rural_electrification_pct', "Taux d'Électrification Rurale (%) - ODD 7"),
                ('mobile_money_penetration_pct', "Inclusion Financière / Mobile Money (%) - ODD 8"),
                ('budget_disbursed_k_eur', "Décaissement des Fonds de Coopération (k€) - ODD 17")
            ],
            format_func=lambda x: x[1]
        )
    with col_sel2:
        horizon = st.slider("Horizon de prévision (mois) :", 6, 24, 12, step=3)
        
    target_var = indicator_choice[0]
    forecast_df, metrics = forecast_time_series(df, target_col=target_var, horizon_months=horizon)
    
    # Cartes de performance de modélisation
    m1, m2, m3, m4 = st.columns(4)
    last_val = df[target_var].iloc[-1]
    final_pred = forecast_df['forecast'].iloc[-1]
    progression = round(final_pred - last_val, 2)
    
    m1.metric("📍 Valeur Actuelle Observée", f"{last_val}")
    m2.metric(f"🎯 Projection à {horizon} mois", f"{final_pred}", delta=f"{'+' if progression > 0 else ''}{progression}")
    m3.metric("📉 Erreur Moyenne (MAPE)", f"{metrics['mape_pct']} %", help="Mean Absolute Percentage Error")
    m4.metric("📈 Gain Annuel Modélisé", f"+{metrics['slope_annual_gain']} pts/an")
    
    # Graphique interactif de séries temporelles avec cône d'incertitude
    st.markdown(f"##### 📊 Historique et Projections Prédictives avec Intervalle de Confiance (95%)")
    fig = go.Figure()
    
    # Série historique
    fig.add_trace(go.Scatter(
        x=df['date'], y=df[target_var],
        mode='lines+markers', name='Données Observées',
        line=dict(color='#0284c7', width=2.5),
        marker=dict(size=5)
    ))
    
    # Cône d'intervalle de confiance
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df['date'], forecast_df['date'][::-1]]),
        y=pd.concat([forecast_df['upper_bound_95'], forecast_df['lower_bound_95'][::-1]]),
        fill='toself',
        fillcolor='rgba(13, 148, 136, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name='Intervalle Confiance 95%'
    ))
    
    # Prévisions
    fig.add_trace(go.Scatter(
        x=forecast_df['date'], y=forecast_df['forecast'],
        mode='lines+markers', name=f'Prévision ({horizon} mois)',
        line=dict(color='#0d9488', width=2.5, dash='dash'),
        marker=dict(symbol='diamond', size=6)
    ))
    
    fig.update_layout(
        xaxis_title="Chronologie Mensuelle",
        yaxis_title="Valeur de l'Indicateur",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=25, b=10),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de données prédictives
    st.markdown("##### 📑 Données Prévisionnelles et Bornes Statistiques")
    st.dataframe(forecast_df.rename(columns={
        'date': 'Mois Prévisionnel',
        'forecast': 'Valeur Estimée',
        'lower_bound_95': 'Borne Inférieure (95%)',
        'upper_bound_95': 'Borne Supérieure (95%)'
    }), use_container_width=True)
