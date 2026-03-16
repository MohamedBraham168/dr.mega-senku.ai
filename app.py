import streamlit as st
from gtts import gTTS
import base64
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Dr. Méga Senku IA", page_icon="🧪")

# Fonction pour la voix (gère les erreurs pour ne pas bloquer l'app)
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
        pass

# --- LOGIQUE DU DIAGNOSTIC ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.index_q = 0
    st.session_state.score = 0

# Les 10 Questions Scientifiques
QUESTIONS = [
    "As-tu une température corporelle supérieure à 38°C ?",
    "Ressens-tu une fatigue anormale ou un manque d'énergie ?",
    "As-tu des maux de tête ou des vertiges ?",
    "As-tu des douleurs au niveau de la gorge ou du cou ?",
    "Est-ce que tu as une toux persistante ?",
    "As-tu des douleurs abdominales ou des nausées ?",
    "As-tu le nez bouché ou des éternuements fréquents ?",
    "As-tu des éruptions cutanées ou des taches sur la peau ?",
    "Ressens-tu une gêne respiratoire ou un essoufflement ?",
    "As-tu perdu le sens de l'odorat ou du goût récemment ?"
]

# Les 50 Maladies
MALADIES = [
    "Grippe", "Angine", "Rhinopharyngite", "Gastro-entérite", "Bronchite", "Otite", "Sinusite", "Appendicite", "Intoxication", 
    "Varicelle", "Rougeole", "Allergie", "Insolation", "Déshydratation", "Conjonctivite", "Migraine", "Cystite", "Asthme", 
    "Laryngite", "Pneumonie", "Coqueluche", "Calcul rénal", "Anémie", "Mononucléose", "Eczéma", "Urticaire", "Sciatique", 
    "Lumbago", "Gale", "Paludisme", "Dengue", "Zika", "Tétanos", "Rachitisme", "Arthrose", "Arthrite", "Goutte", "Ulcère", 
    "Acné sévère", "Insomnie", "Apnée du sommeil", "Dépression", "Anxiété", "Cholestérol", "Hypertension", "Hypotension", 
    "Diabète", "Scorbut", "Rage", "Tuberculose"
]

st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")
robot_place = st.empty()

# --- INTERFACE ET ANIMATIONS ---

if st.session_state.etape == "OFF":
    try: robot_place.image("repos.jpg", width=400)
    except: st.info("Prêt pour l'activation.")
    if st.button("🚀 ACTIVER MÉGA SENKU"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    try: robot_place.image("tenor.gif", width=400)
    except: st.warning("Animation en cours...")
    msg = "Bonjour ! Je suis Méga Senku. Mon analyse est scientifique, mais je reste une IA : consulte un médecin pour confirmer."
    parler(msg)
    st.write(f"💬 **Senku :** {msg}")
    if st.button("COMMENCER LES TESTS ➡️"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    
    st.write(f"### 🔬 Analyse n°{st.session_state.index_q + 1} / 10")
    st.info(QUESTIONS[st.session_state.index_q])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.score += 1
            if st.session_state.index_q < 9:
                st.session_state.index_q += 1
                st.rerun()
            else:
                st.session_state.etape = "RESULTAT"
                st.rerun()
    with col2:
        if st.button("❌ NON"):
            if st.session_state.index_q < 9:
                st.session_state.index_q += 1
                st.rerun()
            else:
                st.session_state.etape = "RESULTAT"
                st.rerun()

elif st.session_state.etape == "RESULTAT":
    try: robot_place.image("tenor.gif", width=400)
    except: pass
    
    # Choix de la maladie basé sur le score pour un semblant de logique
    random.seed(st.session_state.score)
    maladie = random.choice(MALADIES)
    
    if st.session_state.score == 0:
        verdict = "Analyse terminée : Aucun symptôme grave détecté. Repose-toi et bois de l'eau !"
    else:
        verdict = f"D'après mes calculs, il y a une probabilité de {maladie}. C'est scientifiquement l'explication la plus probable parmi mes données."
    
    parler(verdict)
    st.success(f"⚖️ **Verdict :** {verdict}")
    st.error("⚠️ Rappel : Cette IA ne remplace pas un avis médical réel.")
    
    if st.button("🏁 RÉINITIALISER LE LABO"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.score = 0
        st.rerun()
