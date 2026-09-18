"""
Composant Dashboard Streamlit : Analytics Portuaire & Supply Chain AGL
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from .port_data_engine import generate_port_operations_data, compute_port_kpis

def render_port_module():
    st.subheader("🚢 P1 : Pilotage de la Performance Portuaire & Logistique Multimodale (Cible AGL)")
    st.markdown(
        """
        **Cas d'Usage Métier :** Optimisation du temps d'attente en rade (*Turnaround Time*), cadences de manutention 
        portique (*Gross Crane Productivity*) et prévision d'engorgement des terminaux à conteneurs.
        """
    )
    
    # Contrôles interactifs
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])
    with col_ctrl1:
        n_vsl = st.slider("Nombre d'escales analysées :", min_value=50, max_value=300, value=120, step=10)
    with col_ctrl2:
        shipping_filter = st.multiselect("Armateurs :", ['Maersk', 'MSC', 'CMA CGM', 'Hapag-Lloyd', 'COSCO', 'Grimaldi'], default=['Maersk', 'MSC', 'CMA CGM'])
    with col_ctrl3:
        threshold_alert = st.slider("Seuil d'alerte congestion rade (heures) :", 12, 48, 24)
        
    df = generate_port_operations_data(n_vessels=n_vsl)
    if shipping_filter:
        df = df[df['shipping_line'].isin(shipping_filter)]
    df['congestion_alert'] = df['waiting_hours_anchorage'] > threshold_alert
    
    kpis = compute_port_kpis(df)
    
    # Affichage des KPIs majeurs
    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
    kpi_c1.metric("📦 Volume Total Traité", f"{kpis['total_teu_handled']:,} EVP", help="Équivalent Vingt Pieds total manutentionné")
    kpi_c2.metric("⏳ Attente Rade Moyenne", f"{kpis['avg_anchorage_wait_hours']} h", delta=f"{'-' if kpis['avg_anchorage_wait_hours'] < 20 else '+'} vs cible 20h", delta_color="inverse")
    kpi_c3.metric("⏱️ Temps Total Escale (TAT)", f"{kpis['avg_turnaround_time_hours']} h", help="Rade + Opérations quai")
    kpi_c4.metric("⚡ Productivité Portique", f"{kpis['avg_crane_productivity']} EVP/h", delta="+2.3 EVP/h vs standard")
    
    # Graphiques d'analyse
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("##### 📊 Répartition du Volume par Ligne Maritime")
        fig_line = px.bar(df.groupby('shipping_line')['total_teu'].sum().reset_index(),
                          x='shipping_line', y='total_teu', color='shipping_line',
                          labels={'shipping_line': 'Armateur', 'total_teu': 'EVP Total'},
                          color_discrete_sequence=px.colors.qualitative.Prism)
        fig_line.update_layout(showlegend=False, margin=dict(l=10, r=10, t=25, b=10), height=320)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col_chart2:
        st.markdown("##### ⏱️ Temps d'Attente en Rade par Type de Navire")
        fig_box = px.box(df, x='vessel_type', y='waiting_hours_anchorage', color='vessel_type',
                         labels={'vessel_type': 'Type Navire', 'waiting_hours_anchorage': 'Attente Rade (h)'})
        fig_box.update_layout(showlegend=False, margin=dict(l=10, r=10, t=25, b=10), height=320)
        st.plotly_chart(fig_box, use_container_width=True)
        
    # Table des alertes de surestaries (Demurrage)
    st.markdown("##### ⚠️ Alertes Opérationnelles & Risques de Surestaries (Demurrage > Seuil)")
    alerts = df[df['congestion_alert']][['vessel_id', 'vessel_name', 'shipping_line', 'vessel_type', 'waiting_hours_anchorage', 'turnaround_time_hours', 'total_teu', 'berth']]
    st.dataframe(alerts.head(10), use_container_width=True)
