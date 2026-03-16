import streamlit as st
from gtts import gTTS
import base64
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Dr. Méga Senku IA", page_icon="🧪")

# Fonction pour la voix
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("voix.mp3")
    with open("voix.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)

# --- BASE DE DONNÉES DES 50 MALADIES ---
MALADIES = [
    "Grippe", "Angine Blanche", "Angine Rouge", "Rhinopharyngite", "Gastro-entérite", 
    "Bronchite", "Otite", "Sinusite", "Appendicite", "Intoxication alimentaire", 
    "Varicelle", "Rougeole", "Allergie saisonnière", "Insolation", "Déshydratation", 
    "Conjonctivite", "Migraine", "Cystite", "Asthme", "Laryngite",
    "Pneumonie", "Coqueluche", "Calcul rénal", "Anémie", "Mononucléose",
    "Eczéma", "Urticaire", "Sciatique", "Lumbago", "Gale",
    "Paludisme", "Dengue", "Zika", "Tétanos", "Rachitisme",
    "Arthrose", "Arthrite", "Goutte", "Ulcère", "Acné sévère",
    "Insomnie", "Apnée du sommeil", "Dépression", "Anxiété", "Cholestérol",
    "Hypertension", "Hypotension", "Diabète", "Scorbut", "Rage"
]

# --- INITIALISATION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"

url_gif = "https://media.tenor.com/vorWA35Ph3S/mega-senku-talking.gif"
url_repos = "senku_repos.jpg"

st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")
robot_place = st.empty()

# --- LOGIQUE DE L'APPLICATION ---

# ÉTAPE 0 : ACCUEIL
if st.session_state.etape == "OFF":
    robot_place.image(url_repos, width=400)
    st.info("Système en attente d'activation...")
    if st.button("🚀 ACTIVER MÉGA SENKU"):
        st.session_state.etape = "INTRO"
        st.rerun()

# ÉTAPE 1 : INTRODUCTION (BOUCHE OUVERTE)
elif st.session_state.etape == "INTRO":
    robot_place.image(url_gif, width=400)
    msg = "Bonjour ! Je suis Méga Senku. Mon diagnostic est sûr à 10 milliards de pourcent. Prêt pour l'analyse ?"
    parler(msg)
    st.write(f"💬 **Méga Senku :** {msg}")
    if st.button("DÉMARRER L'ANALYSE ➡️"):
        st.session_state.etape = "QUESTION"
        st.rerun()

# ÉTAPE 2 : QUESTION (BOUCHE FERMÉE)
elif st.session_state.etape == "QUESTION":
    robot_place.image(url_repos, width=400)
    st.subheader("🧪 Analyse des symptômes...")
    st.write("Est-ce que vous ressentez une fatigue intense ou de la fièvre ?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.etape = "RESULTAT"
            st.rerun()
    with col2:
        if st.button("❌ NON"):
            st.session_state.etape = "RESULTAT"
            st.rerun()

# ÉTAPE 3 : RÉSULTAT (BOUCHE OUVERTE)
elif st.session_state.etape == "RESULTAT":
    robot_place.image(url_gif, width=400)
    maladie_detectee = random.choice(MALADIES)
    verdict = f"L'analyse est terminée ! Selon mes calculs, c'est une {maladie_detectee}. C'est scientifiquement logique !"
    parler(verdict)
    st.success(f"⚖️ **Verdict :** {verdict}")
    
    if st.button("🏁 TERMINER ET QUITTER"):
        st.session_state.etape = "FIN"
        st.rerun()

# ÉTAPE 4 : DISPARITION
elif st.session_state.etape == "FIN":
    robot_place.image(url_gif, width=400)
    st.write("Désactivation du système... À bientôt !")
    if st.button("🔄 REDÉMARRER"):
        st.session_state.etape = "OFF"
        st.rerun()
