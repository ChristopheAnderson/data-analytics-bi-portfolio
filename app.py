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

import streamlit.components.v1 as components

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
    /* Bouton de fermeture de la barre latérale toujours visible et stylisé */
    [data-testid="stSidebarCollapseButton"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        opacity: 1 !important;
        visibility: visible !important;
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 4px rgba(2,132,199,0.15) !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #0284c7 !important;
        color: #ffffff !important;
        border-color: #0284c7 !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stSidebarCollapseButton"] button::after {
        content: " Masquer";
        font-size: 11px;
        font-weight: 600;
        margin-left: 3px;
    }

    /* Bouton pour rouvrir la barre latérale repliée */
    [data-testid="stSidebarCollapsedControl"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        background: #0f172a !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 6px 12px !important;
        font-weight: 600 !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: #1e3a8a !important;
        color: #ffffff !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stSidebarCollapsedControl"] button::after {
        content: " Menu";
        font-size: 11px;
        font-weight: 600;
        margin-left: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Imports des modules projets
from p1_logistics_port_agl import render_port_module
from p2_marine_spatial_blueventures import render_marine_module
from p3_humanitarian_impact_kobo import render_kobo_module
from p4_predictive_bi_expertise_france import render_predictive_module

def render_cv_module():
    st.markdown("### 📄 Curriculum Vitæ Exécutif — Christophe WAVOEKE")
    st.markdown("**Data Analyst & Spécialiste Business Intelligence / Data Systems**")
    
    cv_pdf_path = os.path.join(CURRENT_DIR, "assets", "cv.pdf")
    cv_html_path = os.path.join(CURRENT_DIR, "assets", "cv.html")
    
    col1, col2, col3 = st.columns([1.5, 1.5, 3])
    with col1:
        if os.path.exists(cv_pdf_path):
            with open(cv_pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le CV (PDF Officiel 2 Pages)",
                    data=f.read(),
                    file_name="CV_Christophe_WAVOEKE_Data_Analyst_BI.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    with col2:
        if os.path.exists(cv_html_path):
            with open(cv_html_path, "r", encoding="utf-8") as f:
                html_data = f.read()
            st.download_button(
                label="🌐 Télécharger la Version HTML Standalone",
                data=html_data,
                file_name="CV_Christophe_WAVOEKE_Data_Analyst_BI.html",
                mime="text/html",
                use_container_width=True
            )
    with col3:
        st.info("💡 **Aperçu haute fidélité :** Le CV interactif complet est intégré ci-dessous avec ses liens cliquables vers les projets opérationnels.")
    
    if os.path.exists(cv_html_path):
        with open(cv_html_path, "r", encoding="utf-8") as f:
            raw_html = f.read()
        components.html(raw_html, height=1250, scrolling=True)
    else:
        st.error("Le fichier du CV HTML est introuvable dans le dossier assets.")

# --- PHOTO DE PROFIL DANS LA BARRE LATÉRALE (RONDE & CENTRÉE) ---
PROFILE_PIC_PATH = None
for p_candidate in [
    os.path.join(CURRENT_DIR, "assets", "jacket.jpeg"),
    os.path.join(CURRENT_DIR, "assets", "profile.jpeg"),
    os.path.join(CURRENT_DIR, "assets", "profile.jpg"),
    os.path.join(CURRENT_DIR, "jacket.jpeg"),
]:
    if os.path.exists(p_candidate):
        PROFILE_PIC_PATH = p_candidate
        break

profile_img_src = ""
if PROFILE_PIC_PATH:
    import base64
    with open(PROFILE_PIC_PATH, "rb") as img_f:
        encoded_photo = base64.b64encode(img_f.read()).decode()
    profile_img_src = f"data:image/jpeg;base64,{encoded_photo}"

# Barre latérale (Sidebar)
with st.sidebar:
    if profile_img_src:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 15px;">
                <img src="{profile_img_src}" alt="Christophe WAVOEKE" style="width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 3px solid #0284c7; box-shadow: 0 4px 14px rgba(2,132,199,0.35);" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)

    st.title("Navigation Portfolio")
    st.markdown("**Christophe WAVOEKE**  \n*Data Analyst & Spécialiste BI*")
    st.caption("📍 Cotonou / Abomey-Calavi, Bénin")
    st.info("💡 **Affichage large :** Cliquez sur **« Masquer** en haut à droite pour replier ce menu et élargir vos graphiques.")
    
    st.divider()
    
    selected_page = st.radio(
        "Sélectionnez une section :",
        [
            "🏠 Vue d'Ensemble du Portfolio",
            "📄 Curriculum Vitæ (CV Exécutif)",
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
    st.markdown("- ⚡ [Plateforme WAPP Énergie](https://power-data-pipeline-bqhbx2x3rta7odtqusg8bb.streamlit.app/)")
    
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
        
    st.info("💡 **Navigation :** Consultez l'onglet **« 📄 Curriculum Vitæ (CV Exécutif) »** pour visualiser et télécharger le CV, ou naviguez sur chaque projet avec ses paramètres ajustables.")

elif selected_page == "📄 Curriculum Vitæ (CV Exécutif)":
    render_cv_module()

elif selected_page == "🚢 P1 : Logistique Portuaire (Cible AGL)":
    render_port_module()

elif selected_page == "🌊 P2 : SIG Marin & Biodiversité (Cible Blue Ventures)":
    render_marine_module()

elif selected_page == "📋 P3 : Audit Qualité Kobo (Cible IMPACT Initiatives)":
    render_kobo_module()

elif selected_page == "📈 P4 : Modélisation ODD (Cible Expertise France / ONU)":
    render_predictive_module()
