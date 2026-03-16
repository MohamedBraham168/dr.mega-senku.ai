import streamlit as st
from gtts import gTTS
import base64
import time
import speech_recognition as sr

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dr. Méga Senku IA", page_icon="🧪", layout="centered")

# --- FONCTIONS TECHNIQUES (VOIX ET MICRO) ---

# Fonction pour générer et jouer la voix
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("voix.mp3")
    with open("voix.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)
    # Calcule un temps de pause approximatif pour que le GIF tourne
    # (environ 1 seconde pour 15 caractères, minimum 2 secondes)
    duree = max(2, len(texte) / 15)
    return duree

# Fonction pour écouter l'utilisateur via le micro
def ecouter_micro():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎤 Je vous écoute...", icon="👂")
        audio = r.listen(source)
        try:
            texte = r.recognize_google(audio, language="fr-FR")
            st.success(f"Vous avez dit : {texte}")
            return texte.lower()
        except sr.UnknownValueError:
            st.error("Désolé, je n'ai pas compris.")
            return ""
        except sr.RequestError:
            st.error("Erreur de connexion au service de reconnaissance vocale.")
            return ""

# --- INITIALISATION DES VARIABLES (CERVEAU DE L'IA) ---
if 'etape' not in st.session_state:
    st.session_state.etape = "apparition" # Étapes : apparition, repos, parle, disparition
    st.session_state.score = 0
    st.session_state.indices_maladies = []
    # Liste simplifiée pour l'exemple, tu peux remettre tes 50 maladies
    st.session_state.maladies = ["Grippe", "Gastro", "Angine", "Appendicite"]
    st.session_state.diag_fini = False
    st.session_state.texte_ia = ""
    st.session_state.choix_user = ""

# --- TITRE DE L'APPLICATION ---
st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")

# --- ZONE D'AFFICHAGE DE MÉGA SENKU (L'IMAGE DYNAMIQUE) ---
robot_place = st.empty()

# URLs des images (Vérifie que 'senku_repos.jpg' est bien sur ton GitHub)
url_gif = "https://media.tenor.com/vorWA35Ph3S/mega-senku-talking.gif"
url_repos = "senku_repos.jpg"

# Logique d'affichage des images selon l'étape
if st.session_state.etape == "apparition":
    robot_place.image(url_gif, width=400, caption="Activation de l'IA...")
    # Laisse le GIF jouer une fois pour l'animation d'entrée (environ 3 secondes)
    time.sleep(3)
    # Parle automatiquement après l'apparition
    st.session_state.texte_ia = "Bonjour ! Je suis Méga Senku. Diagnostique médical à 10 milliards de pourcent. Quel est ton symptôme principal ?"
    st.session_state.etape = "parle"
    st.rerun()

elif st.session_state.etape == "repos":
    robot_place.image(url_repos, width=400, caption="Méga Senku vous écoute...")

elif st.session_state.etape == "parle":
    robot_place.image(url_gif, width=400, caption="Méga Senku réfléchit...")
    duree_voix = parler(st.session_state.texte_ia)
    # Laisse le GIF tourner pendant la durée de la voix
    time.sleep(duree_voix)
    # Après avoir parlé, il écoute
    if st.session_state.diag_fini:
        st.session_state.etape = "disparition"
    else:
        st.session_state.etape = "repos"
    st.rerun()

elif st.session_state.etape == "disparition":
    robot_place.image(url_gif, width=400, caption="Désactivation de l'IA...")
    # Laisse le GIF jouer une fois pour l'animation de sortie (environ 3 secondes)
    time.sleep(3)
    st.session_state.etape = "fin"
    st.rerun()

elif st.session_state.etape == "fin":
    st.write("### Diagnostic Terminé. Merci d'avoir consulté le Dr. Méga Senku.")
    if st.button("Recommencer"):
        st.session_state.etape = "apparition"
        st.session_state.score = 0
        st.session_state.diag_fini = False
        st.rerun()

# --- ZONE D'INTERACTION VOCALE (MICROPHONE) ---
st.divider()

# N'affiche le micro que quand Méga Senku écoute
if st.session_state.etape == "repos":
    st.subheader("🎙️ Discussion Vocale")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 PARLER", help="Cliquez pour utiliser le micro"):
            st.session_state.choix_user = ecouter_micro()
            if st.session_state.choix_user:
                # Logique simplifiée de diagnostic
                if "fièvre" in st.session_state.choix_user:
                    st.session_state.texte_ia = "C'est noté. Fièvre détectée. As-tu aussi mal à la gorge ?"
                elif "oui" in st.session_state.choix_user:
                    st.session_state.texte_ia = "D'accord. Diagnostic probable à 10 milliards de pourcent : c'est une Angine. Prends soin de toi !"
                    st.session_state.diag_fini = True
                else:
                    st.session_state.texte_ia = "Je n'ai pas assez d'informations. Peux-tu préciser ?"
                
                st.session_state.etape = "parle"
                st.rerun()
