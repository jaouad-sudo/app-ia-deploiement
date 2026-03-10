"""
Analyseur CV & Offre d'Emploi
Application Streamlit pour comparer un CV avec une offre d'emploi
"""

import streamlit as st
import pandas as pd
import os
import re
from collections import Counter

# Configuration de la page
st.set_page_config(
    page_title="Analyseur CV & Offre",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Charger les variables d'environnement
APP_TITLE = os.getenv("APP_TITLE", "Analyseur CV & Offre d'Emploi")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Liste des compétences à détecter
COMPETENCES_CLES = [
    "python", "javascript", "react", "sql", "communication", 
    "gestion", "excel", "anglais", "français", "streamlit",
    "java", "docker", "git", "agile", "scrum", "leadership",
    "html", "css", "aws", "azure", "machine learning", "data"
]

def nettoyer_texte(texte):
    """Nettoie et normalise le texte"""
    # Convertir en minuscules
    texte = texte.lower()
    # Extraire uniquement les mots (alphabétiques)
    mots = re.findall(r'\b[a-zàâçéèêëïîôùûüÿæœ]+\b', texte)
    return mots

def detecter_competences(mots):
    """Détecte les compétences dans une liste de mots"""
    texte_complet = ' '.join(mots)
    competences_trouvees = []
    
    for competence in COMPETENCES_CLES:
        if competence in texte_complet:
            competences_trouvees.append(competence)
    
    return competences_trouvees

def calculer_score(mots_cv, mots_offre):
    """Calcule le score de correspondance entre CV et offre"""
    set_cv = set(mots_cv)
    set_offre = set(mots_offre)
    
    # Mots communs
    mots_communs = set_cv.intersection(set_offre)
    
    # Calcul du pourcentage
    if len(set_offre) > 0:
        score = (len(mots_communs) / len(set_offre)) * 100
    else:
        score = 0
    
    return score, mots_communs

def obtenir_message_conseil(score):
    """Retourne un message conseil selon le score"""
    if score > 70:
        return "✅ Excellent alignement ! Votre CV correspond bien à l'offre."
    elif score >= 40:
        return "⚠️ Alignement moyen. Pensez à adapter votre CV pour mieux correspondre à l'offre."
    else:
        return "❌ Faible correspondance. Il est recommandé de retravailler votre CV pour cette offre."

# Interface principale
st.title(f"📄 {APP_TITLE}")
st.caption(f"Version {APP_VERSION}")
st.markdown("---")

# Introduction
st.markdown("""
### 🎯 Bienvenue !
Cette application vous aide à analyser la correspondance entre votre CV et une offre d'emploi.

**Comment ça marche ?**
1. Collez le texte de votre CV dans le premier champ
2. Collez le texte de l'offre d'emploi dans le second champ
3. Cliquez sur **Analyser** pour obtenir vos résultats
""")

st.markdown("---")

# Zone de saisie
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Votre CV")
    cv_text = st.text_area(
        "Collez le texte de votre CV ici",
        height=300,
        placeholder="Exemple: Développeur Python avec 5 ans d'expérience...",
        key="cv"
    )

with col2:
    st.subheader("💼 Offre d'emploi")
    offre_text = st.text_area(
        "Collez le texte de l'offre d'emploi ici",
        height=300,
        placeholder="Exemple: Nous recherchons un développeur Python...",
        key="offre"
    )

# Bouton d'analyse
st.markdown("---")
col_btn = st.columns([2, 1, 2])
with col_btn[1]:
    analyser_btn = st.button("🔍 Analyser", use_container_width=True, type="primary")

# Traitement et affichage des résultats
if analyser_btn:
    # Validation des entrées
    if not cv_text.strip() or not offre_text.strip():
        st.warning("⚠️ Veuillez remplir les deux champs (CV et Offre) avant d'analyser.")
    else:
        st.markdown("---")
        st.subheader("📊 Résultats de l'analyse")
        
        # Nettoyage des textes
        mots_cv = nettoyer_texte(cv_text)
        mots_offre = nettoyer_texte(offre_text)
        
        # Calcul des statistiques
        nb_mots_cv = len(mots_cv)
        nb_mots_offre = len(mots_offre)
        score, mots_communs = calculer_score(mots_cv, mots_offre)
        nb_mots_communs = len(mots_communs)
        
        # Affichage des KPIs
        st.markdown("#### 📈 Statistiques générales")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.metric("Mots dans le CV", nb_mots_cv)
        with kpi2:
            st.metric("Mots dans l'offre", nb_mots_offre)
        with kpi3:
            st.metric("Mots communs", nb_mots_communs)
        with kpi4:
            st.metric("Score de correspondance", f"{score:.1f}%")
        
        # Message conseil
        st.markdown("#### 💡 Conseil")
        message = obtenir_message_conseil(score)
        if score > 70:
            st.success(message)
        elif score >= 40:
            st.warning(message)
        else:
            st.error(message)
        
        # Analyse des compétences
        st.markdown("---")
        st.markdown("#### 🎓 Analyse des compétences")
        
        competences_cv = detecter_competences(mots_cv)
        competences_offre = detecter_competences(mots_offre)
        competences_manquantes = set(competences_offre) - set(competences_cv)
        
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        with col_comp1:
            st.markdown("**✅ Compétences dans votre CV**")
            if competences_cv:
                for comp in sorted(competences_cv):
                    st.markdown(f"- {comp.capitalize()}")
            else:
                st.info("Aucune compétence clé détectée")
        
        with col_comp2:
            st.markdown("**🎯 Compétences demandées**")
            if competences_offre:
                for comp in sorted(competences_offre):
                    st.markdown(f"- {comp.capitalize()}")
            else:
                st.info("Aucune compétence clé détectée")
        
        with col_comp3:
            st.markdown("**⚠️ Compétences manquantes**")
            if competences_manquantes:
                for comp in sorted(competences_manquantes):
                    st.markdown(f"- {comp.capitalize()}")
            else:
                st.success("Aucune compétence manquante !")
        
        # Top 10 des mots fréquents du CV
        st.markdown("---")
        st.markdown("#### 📊 Top 10 des mots les plus fréquents dans votre CV")
        
        # Filtrer les mots trop courts
        mots_cv_filtre = [mot for mot in mots_cv if len(mot) > 3]
        compteur_cv = Counter(mots_cv_filtre)
        top_10 = compteur_cv.most_common(10)
        
        if top_10:
            # Créer un DataFrame pour le graphique
            df_top = pd.DataFrame(top_10, columns=["Mot", "Fréquence"])
            df_top = df_top.set_index("Mot")
            
            # Afficher le graphique
            st.bar_chart(df_top)
        else:
            st.info("Pas assez de données pour générer le graphique")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>Analyseur CV & Offre d'Emploi | Développé avec Streamlit 🚀</p>
    <p style='font-size: 0.8em;'>© 2026 - Outil d'aide à la préparation de candidature</p>
</div>
""", unsafe_allow_html=True)
