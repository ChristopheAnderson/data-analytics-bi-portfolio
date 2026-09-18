"""
Composant Dashboard Streamlit : Analyse Spatiale Marine & Cartographie Côtière (Cible Blue Ventures)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from .marine_spatial_engine import generate_coastal_marine_data, compute_marine_kpis

def render_marine_module():
    st.subheader("🌊 P2 : Analyse Géospatiale Marine & Suivi de la Pêche Artisanale (Cible Blue Ventures)")
    st.markdown(
        """
        **Cas d'Usage Métier :** Cartographie SIG de l'effort de pêche (*CPUE*), bathymétrie côtière,
        surveillance spatiale des Aires Marines Protégées (*AMP*) et analyse d'impact écologique pour les communautés côtières.
        """
    )
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        site_filter = st.multiselect("Secteurs Côtiers d'Étude :", 
                                     ['Baie de Grand-Popo', 'Zone Côtière Ouidah', 'Plateau Cotonou Ouest', 'Banc Sèmè-Kpodji'],
                                     default=['Baie de Grand-Popo', 'Zone Côtière Ouidah', 'Plateau Cotonou Ouest', 'Banc Sèmè-Kpodji'])
    with col_c2:
        gear_filter = st.multiselect("Engins de Pêche :", 
                                     ['Filet maillant dérivant', 'Senne de plage', 'Ligne à main', 'Nasse artisanale'],
                                     default=['Filet maillant dérivant', 'Senne de plage', 'Ligne à main'])
        
    df = generate_coastal_marine_data(n_samples=300)
    if site_filter:
        df = df[df['site_name'].isin(site_filter)]
    if gear_filter:
        df = df[df['gear_type'].isin(gear_filter)]
        
    kpis = compute_marine_kpis(df)
    
    # Indicateurs majeurs
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🐟 Captures Débarquées", f"{kpis['total_catch_tonnes']} Tonnes", help="Volume total échantillonné")
    m2.metric("⚓ Rendement Moyen (CPUE)", f"{kpis['avg_cpue_kg_hr']} kg/h", delta="+12% vs zone dégradée")
    m3.metric("🛡️ Indice Santé en AMP", f"{kpis['eco_health_in_mpa']} / 10", delta=f"+{kpis['biodiversity_gain_pct']}% vs hors AMP", delta_color="normal")
    m4.metric("🗺️ Échantillons en Zone Protégée", f"{kpis['mpa_sample_coverage_pct']}%")
    
    # Cartographie spatiale interactive
    st.markdown("##### 🗺️ Cartographie Spatiale des Prélèvements & Bathymétrie Côtière")
    
    center_lat = float(df['latitude'].mean()) if not df.empty else 6.28
    center_lon = float(df['longitude'].mean()) if not df.empty else 2.38
    
    tab_map1, tab_map2 = st.tabs(["🗺️ Vue Cartographique SIG (OpenStreetMap)", "📍 Projection Spatiale 2D (Coordonnées GPS & Bathymétrie)"])
    
    with tab_map1:
        if hasattr(px, "scatter_map"):
            fig_map = px.scatter_map(
                df,
                lat="latitude",
                lon="longitude",
                color="eco_health_index",
                size="total_catch_kg",
                color_continuous_scale="Viridis",
                size_max=16,
                zoom=9.2,
                center=dict(lat=center_lat, lon=center_lon),
                map_style="open-street-map",
                hover_name="site_name",
                hover_data={"latitude": True, "longitude": True, "bathymetry_m": True, "cpue_kg_hr": True, "in_marine_protected_area": True},
                title="Prélèvements Côtiers : Santé Écologique (Couleur) & Captures kg (Taille)"
            )
        else:
            fig_map = px.scatter_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                color="eco_health_index",
                size="total_catch_kg",
                color_continuous_scale="Viridis",
                size_max=16,
                zoom=9.2,
                center=dict(lat=center_lat, lon=center_lon),
                mapbox_style="open-street-map",
                hover_name="site_name",
                hover_data={"latitude": True, "longitude": True, "bathymetry_m": True, "cpue_kg_hr": True, "in_marine_protected_area": True},
                title="Prélèvements Côtiers : Santé Écologique (Couleur) & Captures kg (Taille)"
            )
        fig_map.update_layout(margin=dict(l=0, r=0, t=35, b=0), height=440)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with tab_map2:
        fig_proj = px.scatter(
            df,
            x="longitude",
            y="latitude",
            color="eco_health_index",
            size="total_catch_kg",
            color_continuous_scale="Viridis",
            labels={"longitude": "Longitude (°E)", "latitude": "Latitude (°N)", "eco_health_index": "Indice Santé (1-10)"},
            hover_name="site_name",
            hover_data={"bathymetry_m": True, "cpue_kg_hr": True, "gear_type": True, "in_marine_protected_area": True},
            title="Projection Spatiale Cartésienne (Plateau Continental Côtier)"
        )
        # Délimitation visuelle de l'Aire Marine Protégée (AMP)
        fig_proj.add_shape(
            type="rect",
            x0=2.25, y0=6.20, x1=2.40, y1=6.28,
            line=dict(color="#0d9488", width=2, dash="dash"),
            fillcolor="rgba(13, 148, 136, 0.12)"
        )
        fig_proj.add_annotation(
            x=2.325, y=6.24, text="Zone Réserve AMP", showarrow=False,
            font=dict(color="#0d9488", size=11, family="sans-serif")
        )
        fig_proj.update_layout(margin=dict(l=10, r=10, t=35, b=10), height=440)
        st.plotly_chart(fig_proj, use_container_width=True)
    
    # Graphiques d'analyse croisée
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 📉 Relation Bathymétrie (Profondeur) vs Rendement (CPUE)")
        try:
            import statsmodels.api as _sm
            fig_scatter = px.scatter(df, x='bathymetry_m', y='cpue_kg_hr', color='gear_type',
                                     labels={'bathymetry_m': 'Profondeur Bathymétrique (m)', 'cpue_kg_hr': 'CPUE (kg/heure)'},
                                     trendline="lowess")
        except (ImportError, ModuleNotFoundError):
            fig_scatter = px.scatter(df, x='bathymetry_m', y='cpue_kg_hr', color='gear_type',
                                     labels={'bathymetry_m': 'Profondeur Bathymétrique (m)', 'cpue_kg_hr': 'CPUE (kg/heure)'})
        fig_scatter.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=300)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_g2:
        st.markdown("##### 🛡️ Comparaison d'Impact : Aire Protégée (AMP) vs Zone Libre")
        comp_df = df.groupby('in_marine_protected_area')[['eco_health_index', 'cpue_kg_hr']].mean().reset_index()
        comp_df['Statut'] = comp_df['in_marine_protected_area'].map({True: 'Aire Marine Protégée (AMP)', False: 'Zone Ouverte'})
        fig_bar = px.bar(comp_df, x='Statut', y='eco_health_index', color='Statut',
                         labels={'eco_health_index': 'Indice Moyen de Santé Écologique (1-10)'},
                         color_discrete_map={'Aire Marine Protégée (AMP)': '#0d9488', 'Zone Ouverte': '#f97316'})
        fig_bar.update_layout(showlegend=False, margin=dict(l=10, r=10, t=20, b=10), height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
