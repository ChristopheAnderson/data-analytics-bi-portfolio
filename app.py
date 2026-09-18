"""
Plateforme Interactive de Démonstration Data Analytics, BI & IA
Auteur : Christophe WAVOEKE - Ingénieur en Génie Mathématique & Informatique
"""

import os
import sys

# Assure que le dossier contenant app.py est dans le PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import streamlit as st

st.set_page_config(
    page_title="Portfolio Projets Data Analytics & BI | Christophe WAVOEKE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0284c7 100%);
        padding: 22px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(15,23,42,0.12);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
    }
    .main-header p {
        margin: 5px 0 0 0;
        color: #cbd5e1;
        font-size: 14px;
    }
    .badge-tag {
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.4);
        display: inline-block;
        margin-top: 6px;
    }
    .project-card {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        background: #ffffff;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Imports des modules projets
from p1_logistics_port_agl import render_port_module
from p2_marine_spatial_blueventures import render_marine_module
from p3_humanitarian_impact_kobo import render_kobo_module
from p4_predictive_bi_expertise_france import render_predictive_module

# Barre latérale (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
    st.title("Navigation Portfolio")
    st.markdown("**Christophe WAVOEKE**  \n*Data Analyst & Spécialiste BI*")
    st.caption("📍 Cotonou / Abomey-Calavi, Bénin")
    
    st.divider()
    
    selected_page = st.radio(
        "Sélectionnez un projet démonstrateur :",
        [
            "🏠 Vue d'Ensemble du Portfolio",
            "🚢 P1 : Logistique Portuaire (Cible AGL)",
            "🌊 P2 : SIG Marin & Biodiversité (Cible Blue Ventures)",
            "📋 P3 : Audit Qualité Kobo (Cible IMPACT Initiatives)",
            "📈 P4 : Modélisation ODD (Cible Expertise France / ONU)"
        ]
    )
    
    st.divider()
    st.markdown("### 🔗 Liens & Contact")
    st.markdown("- 📞 **+229 01 66 81 83 76**")
    st.markdown("- ✉️ [christophewavoeke18@gmail.com](mailto:christophewavoeke18@gmail.com)")
    st.markdown("- 💻 [Portfolio Web](https://christopher-portofolio.vercel.app)")
    st.markdown("- 🐙 [Profil GitHub](https://github.com/ChristopheAnderson)")
    
    st.caption("Plateforme développée sous Python, Streamlit & Plotly.")

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>Plateforme Opérationnelle de Projets Data Analytics & Business Intelligence</h1>
    <p>Démonstrateurs interactifs d'ingénierie décisionnelle, modélisation prédictive et analyse spatiale.</p>
    <span class="badge-tag">Profil Ingénieur : Christophe WAVOEKE</span>
</div>
""", unsafe_allow_html=True)

# Routage des vues
if selected_page == "🏠 Vue d'Ensemble du Portfolio":
    st.markdown("### 🎯 Synthèse des Projets et Références Techniques")
    st.markdown(
        """
        Cette plateforme concrétise l'ensemble des compétences et projets mentionnés sur le CV de 
        **Christophe WAVOEKE** pour répondre avec précision aux exigences des recruteurs et bailleurs internationaux :
        """
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="project-card">
            <h4>🚢 P1 : Logistique Portuaire & Supply Chain Multimodale</h4>
            <p><strong>Cible :</strong> Africa Global Logistics (AGL) / Ports maritimes</p>
            <p>Pilotage du Turnaround Time (temps d'attente rade + quai), cadences portiques EVP/h et détection précoce des risques de surestaries (Demurrage).</p>
            <small><strong>Stack :</strong> Python, SQL, KPI Analytics, Plotly</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="project-card">
            <h4>📋 P3 : Pipeline d'Audit Qualité & Data Humanitaire Kobo</h4>
            <p><strong>Cible :</strong> IMPACT Initiatives / REACH / ONG Internationales</p>
            <p>Ingestion de données mobiles Kobo/ODK, contrôle qualité automatisé (Speeding surveys, logique démographique, outliers) et génération du Cleaning Log.</p>
            <small><strong>Stack :</strong> Python, Data Quality Rules, Validation Statistique</small>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="project-card">
            <h4>🌊 P2 : Analyse Géospatiale & Cartographie Côtière (SIG)</h4>
            <p><strong>Cible :</strong> Blue Ventures / Projets Environnement & Pêche</p>
            <p>Cartographie spatio-temporelle de l'effort de pêche côtière (CPUE), bathymétrie, suivi des Aires Marines Protégées (AMP) et analyse d'impact écologique.</p>
            <small><strong>Stack :</strong> GeoPandas, Scatter Mapbox, Géostatistique, Folium</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="project-card">
            <h4>📈 P4 : Modélisation Prévisionnelle & Indicateurs ODD</h4>
            <p><strong>Cible :</strong> Expertise France / Système des Nations Unies (ONU)</p>
            <p>Analyse prédictive de séries temporelles avec décomposition de tendance et saisonnalité, cônes de confiance à 95% et suivi décisionnel des ODD.</p>
            <small><strong>Stack :</strong> Time Series Forecasting, Scikit-Learn, Streamlit Dataviz</small>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 **Navigation :** Utilisez le menu latéral à gauche pour tester en direct chaque projet avec ses paramètres ajustables.")

elif selected_page == "🚢 P1 : Logistique Portuaire (Cible AGL)":
    render_port_module()

elif selected_page == "🌊 P2 : SIG Marin & Biodiversité (Cible Blue Ventures)":
    render_marine_module()

elif selected_page == "📋 P3 : Audit Qualité Kobo (Cible IMPACT Initiatives)":
    render_kobo_module()

elif selected_page == "📈 P4 : Modélisation ODD (Cible Expertise France / ONU)":
    render_predictive_module()
