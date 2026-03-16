import streamlit as st
from gtts import gTTS
import base64
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs MÉDECIN", page_icon="🧪")

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

# --- INITIALISATION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.index_q = 0
    st.session_state.score = 0

# LES QUESTIONS (Précises pour simuler un vrai diagnostic)
QUESTIONS = [
    "Température supérieure à 38.5°C ?",
    "Fatigue intense empêchant de se lever ?",
    "Douleurs thoraciques ou essoufflement ?",
    "Gorge inflammée ou ganglions gonflés ?",
    "Toux persistante avec sécrétions ?",
    "Douleurs abdominales aiguës ?",
    "Nez bouché et perte d'odorat ?",
    "Éruptions cutanées ou taches bizarres ?",
    "Douleurs articulaires ou courbatures ?",
    "Maux de tête violents et sensibilité à la lumière ?"
]

# LISTE DES 50 MALADIES
MALADIES = [
    "Grippe", "Angine", "Rhinopharyngite", "Gastro-entérite", "Bronchite", "Otite", "Sinusite", "Appendicite", "Intoxication", 
    "Varicelle", "Rougeole", "Allergie", "Insolation", "Déshydratation", "Conjonctivite", "Migraine", "Cystite", "Asthme", 
    "Laryngite", "Pneumonie", "Coqueluche", "Calcul rénal", "Anémie", "Mononucléose", "Eczéma", "Urticaire", "Sciatique", 
    "Lumbago", "Gale", "Paludisme", "Dengue", "Zika", "Tétanos", "Rachitisme", "Arthrose", "Arthrite", "Goutte", "Ulcère", 
    "Acné sévère", "Insomnie", "Apnée du sommeil", "Dépression", "Anxiété", "Cholestérol", "Hypertension", "Hypotension", 
    "Diabète", "Scorbut", "Rage", "Tuberculose"
]

st.title("👨‍🔬 Dr. Méga Senku - IA Médicale")
st.write("**Problématique : L'IA peut-elle surpasser le diagnostic humain ?**")
robot_place = st.empty()

# --- INTERFACE ---

if st.session_state.etape == "OFF":
    robot_place.image("repos.jpg", width=400)
    if st.button("🚀 ACTIVER LE CERVEAU ARTIFICIEL"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    robot_place.image("tenor.gif", width=400)
    msg = "L'humain fait des erreurs, la science n'en fait pas. Je vais prouver que mon algorithme est plus efficace qu'un médecin de campagne. Analyse prête à 10 milliards de pourcent !"
    parler(msg)
    st.write(f"💬 **Senku :** {msg}")
    if st.button("LANCER LE DIAGNOSTIC"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    robot_place.image("repos.jpg", width=400)
    st.write(f"### Collecte de données n°{st.session_state.index_q + 1} / 10")
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
    robot_place.image("tenor.gif", width=400)
    
    # Choix de la maladie
    random.seed(st.session_state.score)
    maladie = random.choice(MALADIES)
    
    if st.session_state.score == 0:
        verdict = "Mes capteurs n'indiquent aucune anomalie biologique. Ton corps est sain. Pas besoin d'un humain pour confirmer l'évidence !"
    else:
        verdict = f"Diagnostic final : {maladie}. Ma précision logicielle dépasse les capacités d'un cerveau humain fatigué. La médecine du futur est là !"
    
    parler(verdict)
    st.success(verdict)
    
    st.write("---")
    st.markdown("*Note de l'exposé : Cet exemple montre comment l'IA peut s'affirmer, mais soulève la question de la responsabilité légale sans humain derrière.*")
    
    if st.button("🏁 RÉINITIALISER"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.score = 0
        st.rerun()
