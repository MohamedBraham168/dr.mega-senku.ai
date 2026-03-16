import streamlit as st
from gtts import gTTS
import base64
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs Humain", page_icon="🧪")

# Fonction son (avec sécurité)
def parler(texte):
    try:
        tts = gTTS(text=texte, lang='fr')
        tts.save("voix.mp3")
        with open("voix.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
    except:
        st.write("*(Lecture audio en cours...)*")

# --- INITIALISATION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.index_q = 0
    st.session_state.score = 0

# LES QUESTIONS (10 questions stratégiques)
QUESTIONS = [
    "Avez-vous une température supérieure à 38°C ?",
    "Ressentez-vous une fatigue intense ?",
    "Avez-vous des maux de tête ?",
    "Avez-vous mal à la gorge ?",
    "Avez-vous une toux persistante ?",
    "Avez-vous des douleurs abdominales ?",
    "Avez-vous le nez bouché ?",
    "Avez-vous des plaques rouges sur la peau ?",
    "Avez-vous du mal à respirer ?",
    "Avez-vous perdu le goût ou l'odorat ?"
]

MALADIES = ["Grippe", "Angine", "Rhinopharyngite", "Gastro-entérite", "Bronchite", "Otite", "Sinusite", "Allergie", "Migraine", "Asthme", "Pneumonie", "Mononucléose", "Diabète", "Anémie", "Insolation"]

# --- AFFICHAGE ---
st.markdown("# 👨‍🔬 Dr. Méga Senku - IA Médicale")
st.markdown("### 🔍 Problématique : L'IA peut-elle remplacer l'humain dans le diagnostic ?")
st.divider()

robot_place = st.empty()

# Gestion des images avec sécurité pour éviter l'écran rouge
def charger_image(nom):
    try:
        robot_place.image(nom, width=400)
    except:
        robot_place.warning(f"Chargement de l'image {nom}...")

# --- LOGIQUE ---

if st.session_state.etape == "OFF":
    charger_image("repos.jpg")
    if st.button("🚀 ACTIVER L'IA"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    charger_image("tenor.gif")
    msg = "L'analyse humaine est lente. Mon algorithme est instantané. Je vais prouver que l'IA est le futur de la médecine. Commençons à 10 milliards de pourcent !"
    st.write(f"**Senku :** {msg}")
    parler(msg)
    if st.button("DÉMARRER LES TESTS"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    charger_image("repos.jpg")
    st.write(f"**Question {st.session_state.index_q + 1} / 10**")
    st.info(QUESTIONS[st.session_state.index_q])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.score += 1
            if st.session_state.index_q < 9: st.session_state.index_q += 1
            else: st.session_state.etape = "RESULTAT"
            st.rerun()
    with col2:
        if st.button("❌ NON"):
            if st.session_state.index_q < 9: st.session_state.index_q += 1
            else: st.session_state.etape = "RESULTAT"
            st.rerun()

elif st.session_state.etape == "RESULTAT":
    charger_image("tenor.gif")
    diag = random.choice(MALADIES) if st.session_state.score > 0 else "Parfaite santé"
    verdict = f"Résultat : {diag}. Mon diagnostic est sans appel. L'humain est-il encore nécessaire ?"
    st.success(verdict)
    parler(verdict)
    
    if st.button("🔄 TESTER À NOUVEAU"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.score = 0
        st.rerun()
