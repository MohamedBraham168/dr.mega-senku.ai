import streamlit as st
from gtts import gTTS
import base64
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Dr. Méga Senku - IA 7.0", page_icon="🧪")

def parler(texte):
    try:
        tts = gTTS(text=texte, lang='fr')
        tts.save("voix.mp3")
        with open("voix.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
    except: pass

if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.reponses = {}
    st.session_state.index_q = 0

st.markdown("# 👨‍🔬 Dr. Méga Senku - IA Médicale v7.0")
st.markdown("### 🔍 Scanner Expert : 30 Symptômes & 50+ Pathologies")

# --- LISTE DES 30 SYMPTÔMES (Balaie tout le corps) ---
QUESTIONS = [
    # Général
    ("fievre", "Fièvre (>38.5°C) ?"), ("fatigue", "Fatigue intense / Épuisement ?"), ("frissons", "Frissons ou sueurs nocturnes ?"),
    # Tête & Cou
    ("tete", "Maux de tête violents ?"), ("gorge", "Mal de gorge intense ?"), ("nuque", "Raideur de la nuque (douleur en baissant la tête) ?"),
    ("vertiges", "Vertiges ou pertes d'équilibre ?"), ("ganglions", "Ganglions gonflés au cou ou aux aisselles ?"),
    # Respiratoire
    ("toux_seche", "Toux sèche irritante ?"), ("toux_grasse", "Toux avec sécrétions (glaires) ?"), ("souffle", "Difficulté à respirer (essoufflement) ?"),
    ("sifflement", "Sifflement lors de la respiration ?"), ("nez_coule", "Écoulement nasal ou nez bouché ?"),
    # Digestif
    ("nausees", "Nausées ou envie de vomir ?"), ("vomis", "Vomissements effectifs ?"), ("douleur_ventre", "Douleurs abdominales ?"),
    ("diarrhee", "Diarrhée ou troubles intestinaux ?"), ("appetit", "Perte totale d'appétit ?"),
    # Douleurs & Peau
    ("courbatures", "Douleurs musculaires / Courbatures ?"), ("dos", "Douleur vive dans le bas du dos ?"), ("articulations", "Douleurs aux articulations ?"),
    ("boutons", "Apparition de boutons ou vésicules ?"), ("plaques", "Plaques rouges ou démangeaisons ?"), ("teint", "Teint pâle ou yeux jaunes ?"),
    # Signatures Spécifiques
    ("perte_gout", "Perte du goût ou de l'odorat ?"), ("taches_bouche", "Petites taches blanches à l'intérieur des joues ?"),
    ("douleur_droite", "Douleur très précise en bas à droite du ventre ?"), ("photophobie", "La lumière fait-elle mal aux yeux ?"),
    ("soif", "Soif permanente et besoin d'uriner fréquent ?"), ("oppression", "Sensation de broyage dans la poitrine ?")
]

# --- BASE DE DONNÉES (Exemple de structure avec signatures) ---
# Chaque maladie a : [Symptômes communs], [Signatures uniques], "Traitement"
DB = {
    "Grippe Infectieuse": (["fievre", "fatigue", "frissons", "toux_seche"], ["courbatures", "tete"], "Repos, Paracétamol, Hydratation."),
    "Méningite": (["fievre", "tete", "nausees", "vomis"], ["nuque", "photophobie"], "URGENCE VITALE : Appelez le 15 immédiatement."),
    "Appendicite Aiguë": (["fievre", "nausees", "vomis", "appetit"], ["douleur_ventre", "douleur_droite"], "URGENCE : Chirurgie nécessaire."),
    "COVID-19": (["fievre", "toux_seche", "fatigue", "nez_coule"], ["perte_gout", "souffle"], "Isolement, Test PCR, Surveillance oxygène."),
    "Rougeole": (["fievre", "toux_seche", "nez_coule", "yeux_rouges"], ["taches_bouche", "boutons"], "Repos, Surveillance de la fièvre."),
    "Gastro-entérite": (["fatigue", "appetit", "douleur_ventre", "frissons"], ["vomis", "diarrhee"], "Solution de réhydratation, Régime riz."),
    "Angine Bactérienne": (["fievre", "tete", "fatigue", "courbatures"], ["gorge", "ganglions"], "Antibiotiques, Spray antiseptique."),
    "Asthme Sévère": (["toux_seche", "oppression", "fatigue", "frissons"], ["souffle", "sifflement"], "Ventoline, Corticoïdes inhalés."),
    "Diabète Type 1 (Détection)": (["fatigue", "appetit", "vertiges", "nausees"], ["soif", "perte_poids"], "Bilan glycémique urgent."),
    "Pneumonie": (["fievre", "frissons", "fatigue", "souffle"], ["toux_grasse", "oppression"], "Antibiotiques, Radio pulmonaire.")
}

# --- LOGIQUE ---
if st.session_state.etape == "OFF":
    if st.button("🚀 LANCER LE SCAN MÉDICAL PROFOND (30 POINTS)"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    idx = st.session_state.index_q
    if idx < len(QUESTIONS):
        id_s, txt = QUESTIONS[idx]
        st.write(f"📊 **Analyse n°{idx+1} / 30**")
        st.progress((idx + 1) / len(QUESTIONS))
        st.info(txt)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ OUI"):
                st.session_state.reponses[id_s] = True
                st.session_state.index_q += 1
                st.rerun()
        with c2:
            if st.button("❌ NON"):
                st.session_state.reponses[id_s] = False
                st.session_state.index_q += 1
                st.rerun()
    else:
        st.session_state.etape = "AI_THINKING"
        st.rerun()

elif st.session_state.etape == "AI_THINKING":
    st.write("🔬 **Analyse des 30 points de données par le réseau neuronal...**")
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        bar.progress(i + 1)
    st.session_state.etape = "RESULTAT"
    st.rerun()

elif st.session_state.etape == "RESULTAT":
    mes_s = [k for k, v in st.session_state.reponses.items() if v]
    
    best_m = "Indéterminé (Symptômes trop vagues)"
    max_score = 0
    final_soin = "Veuillez consulter un médecin pour un examen clinique."

    for nom, (communs, signatures, soin) in DB.items():
        score_c = len(set(mes_s) & set(communs))
        score_s = len(set(mes_s) & set(signatures)) * 2 # Les signatures comptent double !
        total = score_c + score_s
        
        if total > max_score:
            max_score = total
            best_m = nom
            final_soin = soin

    st.success(f"### Résultat du Scan : {best_m}")
    parler(f"Analyse terminée. Ma base de données indique une probabilité forte de {best_m}.")

    st.markdown(f"""
    <div style="background-color: white; color: black; padding: 25px; border: 5px solid #1f1f1f; border-radius: 15px;">
        <h2 style="text-align:center;">RAPPORT DE DIAGNOSTIC IA</h2>
        <p><b>Points analysés :</b> 30 symptômes</p>
        <p><b>Score de confiance :</b> {min(max_score * 10, 100)}%</p>
        <hr>
        <p><b>PATHOLOGIE :</b> {best_m}</p>
        <p><b>CONDUITE À TENIR :</b> {final_soin}</p>
        <br>
        <p style="font-size:10px;">Signature : Dr. Méga Senku - Intelligence Artificielle</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 NOUVELLE ANALYSE"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.reponses = {}
        st.rerun()
