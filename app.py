import streamlit as st
from gtts import gTTS
import base64
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Dr. Méga Senku", page_icon="🧪")

# --- FONCTION VOIX ---
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("voix.mp3")
    with open("voix.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)

# --- INITIALISATION DU CERVEAU (LES 50 MALADIES) ---
if 'maladies' not in st.session_state:
    st.session_state.liste_maladies = [
        "Grippe", "Angine", "Gastro", "Bronchite", "Otite", "Sinusite", "Appendicite", "Intoxication", 
        "Varicelle", "Rougeole", "Allergie", "Insolation", "Déshydratation", "Conjonctivite", "Migraine", 
        "Cystite", "Asthme", "Laryngite", "Pneumonie", "Coqueluche", "Calcul rénal", "Anémie", 
        "Mononucléose", "Eczéma", "Urticaire", "Sciatique", "Lumbago", "Gale", "Paludisme", "Dengue", 
        "Zika", "Tétanos", "Rachitisme", "Arthrose", "Arthrite", "Goutte", "Ulcère", "Acné", "Insomnie", 
        "Apnée du sommeil", "Dépression", "Anxiété", "Cholestérol", "Hypertension", "Hypotension", 
        "Diabète", "Scorbut", "Rage", "Tuberculose", "Rhumatisme"
    ]
    st.session_state.etape = "OFF"
    st.session_state.score = 0
    st.session_state.index_q = 0

# --- IMAGES ---
url_gif = "https://media.tenor.com/vorWA35Ph3S/mega-senku-talking.gif"
url_repos = "senku_repos.jpg"

st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")
robot_place = st.empty()

# --- LOGIQUE DE L'ANIMATION ET DU DIAGNOSTIC ---

# 1. ÉCRAN D'ACCUEIL
if st.session_state.etape == "OFF":
    st.write("### Prêt pour le diagnostic scientifique ?")
    if st.button("🚀 ACTIVER MÉGA SENKU"):
        st.session_state.etape = "APPARITION"
        st.rerun()

# 2. ANIMATION D'APPARITION (GIF monte)
elif st.session_state.etape == "APPARITION":
    robot_place.image(url_gif, width=400)
    time.sleep(3) # Temps du GIF qui monte
    st.session_state.etape = "INTRO"
    st.rerun()

# 3. INTRODUCTION PARLÉE (GIF bouche ouverte)
elif st.session_state.etape == "INTRO":
    robot_place.image(url_gif, width=400)
    msg = "Bonjour ! Je suis Méga Senku. Mon diagnostic est sûr à 10 milliards de pourcent. Dis-moi, as-tu de la fièvre ?"
    parler(msg)
    time.sleep(7) # Laisse le temps de parler
    st.session_state.etape = "QUESTION"
    st.rerun()

# 4. PHASE DE QUESTIONS (Image fixe bouche fermée)
elif st.session_state.etape == "QUESTION":
    robot_place.image(url_repos, width=400)
    st.write("### Répondez honnêtement :")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.score += 1
            st.session_state.etape = "RESULTAT"
            st.rerun()
    with col2:
        if st.button("❌ NON"):
            st.session_state.etape = "RESULTAT"
            st.rerun()

# 5. RÉSULTAT (GIF bouche ouverte pour parler)
elif st.session_state.etape == "RESULTAT":
    robot_place.image(url_gif, width=400)
    import random
    maladie = random.choice(st.session_state.liste_maladies)
    verdict = f"Après analyse scientifique, tu as probablement une {maladie} ! C'est logique !"
    parler(verdict)
    time.sleep(6)
    st.session_state.etape = "DISPARITION"
    st.rerun()

# 6. ANIMATION DE DISPARITION (GIF descend)
elif st.session_state.etape == "DISPARITION":
    robot_place.image(url_gif, width=400)
    time.sleep(3) # Temps du GIF qui descend
    st.session_state.etape = "FIN"
    st.rerun()

# 7. ÉCRAN FINAL
elif st.session_state.etape == "FIN":
    st.success("Diagnostic terminé.")
    if st.button("🔄 Redémarrer l'IA"):
        st.session_state.etape = "OFF"
        st.session_state.score = 0
        st.rerun()
