import streamlit as st
from gtts import gTTS
import base64
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dr. Méga Senku IA", page_icon="🧪")

# --- FONCTION VOIX ---
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("voix.mp3")
    with open("voix.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)

# --- LE CERVEAU : LES 50 MALADIES ---
if 'scores' not in st.session_state:
    maladies = [
        "Grippe", "Angine Blanche", "Angine Rouge", "Rhinopharyngite", "Gastro", 
        "Bronchite", "Otite", "Sinusite", "Appendicite", "Intoxication", 
        "Varicelle", "Rougeole", "Allergie", "Insolation", "Déshydratation", 
        "Conjonctivite", "Migraine", "Cystite", "Asthme", "Laryngite",
        "Pneumonie", "Coqueluche", "Calcul rénal", "Anémie", "Mononucléose",
        "Eczéma", "Urticaire", "Sciatique", "Lumbago", "Gale",
        "Paludisme", "Dengue", "Zika", "Tétanos", "Rachitisme",
        "Arthrose", "Arthrite", "Goutte", "Ulcère", "Acné",
        "Insomnie", "Apnée du sommeil", "Dépression", "Anxiété", "Cholestérol",
        "Hypertension", "Hypotension", "Diabète", "Scurvy", "Rage"
    ]
    st.session_state.scores = {m: 0 for m in maladies}
    st.session_state.idx = 0
    st.session_state.fini = False
    st.session_state.parle = False

# --- INTERFACE VISUELLE ---
st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")

robot_place = st.empty()

# Gestion des images (Assure-toi d'avoir ces fichiers sur GitHub)
if st.session_state.parle:
    # Le GIF (bouche ouverte/mouvement)
    robot_place.image("https://media.tenor.com/vorWA35Ph3S/mega-senku-talking.gif", width=400)
else:
    # L'image que je viens de te faire (bouche fermée)
    # Renomme ton image 'senku_repos.jpg' sur GitHub
    robot_place.image("senku_repos.jpg", width=400)

# --- LOGIQUE DU QUESTIONNAIRE ---
questions = [
    ("Bonjour ! Je suis Méga Senku. Dites-moi, avez-vous de la fièvre ?", ["Grippe", "Angine Blanche", "Angine Rouge", "Otite", "Pneumonie", "Paludisme"]),
    ("Avez-vous des douleurs abdominales ?", ["Gastro", "Appendicite", "Intoxication", "Ulcère", "Calcul rénal"]),
    ("Avez-vous des boutons ou des rougeurs ?", ["Varicelle", "Rougeole", "Eczéma", "Urticaire", "Zika"]),
    ("Est-ce que votre gorge est douloureuse ?", ["Angine Blanche", "Angine Rouge", "Laryngite", "Rhinopharyngite"]),
    ("Avez-vous du mal à respirer ?", ["Asthme", "Bronchite", "Pneumonie", "Coqueluche"]),
    ("Souffrez-vous de maux de tête ?", ["Migraine", "Sinusite", "Hypertension", "Insolation"]),
]

if not st.session_state.fini and st.session_state.idx < len(questions):
    q_texte, cibles = questions[st.session_state.idx]
    
    st.write(f"### 💬 Question : {q_texte}")
    
    if st.button("▶️ ÉCOUTER L'IA"):
        st.session_state.parle = True
        parler(q_texte)
        # On simule un temps de parole avant de fermer la bouche
        # time.sleep(2) # Enlevé pour éviter les bugs Streamlit, l'image changera au prochain clic

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.parle = False
            for m in cibles: st.session_state.scores[m] += 1
            gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
            if st.session_state.scores[gagnant] >= 2: st.session_state.fini = True
            else: st.session_state.idx += 1
            st.rerun()
    with col2:
        if st.button("❌ NON"):
            st.session_state.parle = False
            st.session_state.idx += 1
            st.rerun()
else:
    st.session_state.fini = True
    gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
    resultat = f"Diagnostic de Méga Senku : C'est une {gagnant} ! 10 milliards de pourcent de certitude !"
    st.success(resultat)
    if st.button("🔊 Entendre le verdict"):
        parler(resultat)
    
    if st.button("Recommencer"):
        st.session_state.scores = {m: 0 for m in st.session_state.scores}
        st.session_state.idx = 0
        st.session_state.fini = False
        st.rerun()
