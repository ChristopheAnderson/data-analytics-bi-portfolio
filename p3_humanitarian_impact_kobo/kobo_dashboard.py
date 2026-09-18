"""
Composant Dashboard Streamlit : Audit Qualité & Données Humanitaires (Cible IMPACT Initiatives / REACH)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from .kobo_audit_engine import generate_humanitarian_survey_data, audit_humanitarian_data

def render_kobo_module():
    st.subheader("📋 P3 : Pipeline d'Audit Qualité & Data Humanitaire KoboToolbox / ODK (Cible IMPACT Initiatives)")
    st.markdown(
        """
        **Cas d'Usage Métier :** Traitement de données d'enquêtes de terrain (*MSNA*), détection automatisée
        des erreurs d'enquêteurs (*Speeding*, incohérences démographiques, *outliers* statistiques) et production du *Cleaning Log*.
        """
    )
    
    col_k1, col_k2 = st.columns([1, 1])
    with col_k1:
        n_surveys = st.slider("Taille de l'échantillon d'enquêtes :", 150, 600, 350, step=50)
    with col_k2:
        dept_selected = st.multiselect("Départements cibles :", 
                                       ['Alibori', 'Atacora', 'Borgou', 'Zou', 'Littoral'],
                                       default=['Alibori', 'Atacora', 'Borgou'])
        
    df = generate_humanitarian_survey_data(n_surveys=n_surveys)
    if dept_selected:
        df = df[df['department'].isin(dept_selected)]
        
    audit_res = audit_humanitarian_data(df)
    
    # Indicateurs qualité
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("📝 Questionnaires Soumis", f"{audit_res['total_surveys']}")
    q2.metric("🛡️ Indice Qualité Global", f"{audit_res['data_quality_score_pct']} %", delta=f"{'+' if audit_res['data_quality_score_pct'] >= 90 else '-'} Seuil 90%")
    q3.metric("⚡ Enquêtes Rapides (<15 min)", f"{audit_res['speeding_count']}", delta="Speeding check", delta_color="inverse")
    q4.metric("❌ Erreurs de Logique Démographique", f"{audit_res['logic_errors_count']}", delta_color="inverse")
    
    # Visualisation des scores de sécurité alimentaire (FCS) et vulnérabilité
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("##### 🍲 Profil de Consommation Alimentaire (FCS) par Département")
        fig_fcs = px.violin(df, x='department', y='fcs_food_consumption', color='department', box=True, points="all",
                            labels={'fcs_food_consumption': 'Score FCS', 'department': 'Département'})
        # Lignes seuils PAM
        fig_fcs.add_hline(y=21, line_dash="dash", line_color="red", annotation_text="Pauvre (<=21)")
        fig_fcs.add_hline(y=35, line_dash="dash", line_color="orange", annotation_text="Limite (<=35)")
        fig_fcs.update_layout(showlegend=False, margin=dict(l=10, r=10, t=25, b=10), height=320)
        st.plotly_chart(fig_fcs, use_container_width=True)
        
    with col_v2:
        st.markdown("##### ⏱️ Distribution des Durées d'Interview par Enquêteur")
        fig_dur = px.box(df, x='enumerator_id', y='survey_duration_min',
                         labels={'survey_duration_min': 'Durée (min)', 'enumerator_id': 'Code Enquêteur'})
        fig_dur.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Seuil Speeding (15 min)")
        fig_dur.update_layout(margin=dict(l=10, r=10, t=25, b=10), height=320)
        st.plotly_chart(fig_dur, use_container_width=True)
        
    # Table du Cleaning Log généré
    st.markdown("##### 📋 Journal d'Audit & Recommandations de Nettoyage (Cleaning Log Automatisé)")
    clean_log = audit_res['cleaning_log']
    if not clean_log.empty:
        st.dataframe(clean_log.head(15), use_container_width=True)
    else:
        st.success("✅ Aucune anomalie détectée sur le sous-ensemble sélectionné.")
