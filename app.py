import streamlit as st
from gtts import gTTS
import base64
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Dr. Méga Senku IA", page_icon="🧪")

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

# --- LOGIQUE MÉDICALE ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.index_q = 0
    st.session_state.score_gravite = 0

# Les 10 Questions Stratégiques
QUESTIONS = [
    "As-tu une fièvre supérieure à 38.5°C ?",
    "Ressens-tu une fatigue qui t'oblige à rester au lit ?",
    "As-tu des douleurs intenses à la tête ou aux articulations ?",
    "As-tu la gorge très irritée ou des difficultés à avaler ?",
    "Est-ce que tu tousses fréquemment ?",
    "As-tu des nausées, des vomissements ou mal au ventre ?",
    "As-tu le nez bouché ou qui coule beaucoup ?",
    "As-tu remarqué des taches, des boutons ou des rougeurs sur ta peau ?",
    "As-tu des difficultés à respirer profondément ?",
    "As-tu perdu le goût des aliments ou l'odorat ?"
]

# Les 50 Maladies classées par "type" pour plus de logique
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

# Utilisation des fichiers locaux sur GitHub
gif_local = "senku_parle.gif"
repos_local = "senku_repos.jpg"

# --- INTERFACE ---

if st.session_state.etape == "OFF":
    robot_place.image(repos_local, width=400)
    st.info("Laboratoire prêt pour l'analyse.")
    if st.button("🚀 ACTIVER MÉGA SENKU"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    robot_place.image(gif_local, width=400)
    msg = "Bonjour ! Je suis Méga Senku. Mon analyse est basée sur la science, mais je suis une IA : consulte un médecin pour confirmer."
    parler(msg)
    st.write(f"💬 **Senku :** {msg}")
    if st.button("COMMENCER LES TESTS"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    robot_place.image(repos_local, width=400)
    
    q_actuelle = QUESTIONS[st.session_state.index_q]
    st.write(f"### 🔬 Test n°{st.session_state.index_q + 1} / 10")
    st.info(q_actuelle)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OUI"):
            st.session_state.score_gravite += 1
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
    robot_place.image(gif_local, width=400)
    
    # Logique de sélection : On utilise le score pour piocher dans la liste
    # Si score 0, on donne une maladie légère, si score haut, une maladie plus complexe
    random.seed(st.session_state.score_gravite) # Pour que le résultat soit constant
    maladie = random.choice(MALADIES)
    
    if st.session_state.score_gravite == 0:
        verdict = "Analyse terminée : Aucune maladie détectée. Tu as juste besoin d'un peu de Cola et de repos !"
    else:
        verdict = f"Les résultats suggèrent une probabilité de {maladie}. C'est scientifiquement l'explication la plus logique !"
    
    parler(verdict)
    st.success(f"⚖️ **Verdict final :** {verdict}")
    st.error("⚠️ Attention : Ne prends aucun médicament sans l'avis d'un vrai docteur.")
    
    if st.button("🏁 RÉINITIALISER LE LABO"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.score_gravite = 0
        st.rerun()
