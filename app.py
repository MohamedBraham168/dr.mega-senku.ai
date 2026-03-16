import streamlit as st
from gtts import gTTS
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs MÉDECIN - Diagnostic Expert", page_icon="🧪")

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

if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.chemin = ""

st.markdown("# 👨‍🔬 Dr. Méga Senku - Système Expert")
st.markdown("### 🔍 Problématique : L'IA peut-elle remplacer l'humain ?")
st.divider()

robot_place = st.empty()

# --- BASE DE DONNÉES : TRAITEMENTS ET ORDONNANCES ---
SOINS = {
    "Grippe": "Repos strict, hydratation (2L/jour) et paracétamol 1g toutes les 6h.",
    "Pneumonie": "Antibiothérapie ciblée et surveillance de la saturation en oxygène.",
    "Angine bactérienne": "Traitement antibiotique (Amoxicilline) et spray buccal antiseptique.",
    "Appendicite": "URGENT : Hospitalisation immédiate pour appendicectomie chirurgicale.",
    "Migraine sévère": "Triptans, repos dans le noir complet et hydratation.",
    "Gastro-entérite": "Solution de réhydratation et régime riz/carottes pendant 48h.",
    "Asthme": "Utilisation immédiate d'un bronchodilatateur (Ventoline).",
    "Anémie (manque de fer)": "Supplémentation en fer et consommation de viande rouge/lentilles.",
    "Simple fatigue ou Stress intense": "Cure de Magnésium et régulation du cycle de sommeil.",
    "Varicelle": "Antihistaminique pour les démangeaisons et désinfectant local."
}

# --- L'ARBRE DE DÉCISION ---
ARBRE = {
    "": "Avez-vous de la fièvre ?",
    "O": "La fièvre est-elle supérieure à 39°C ?",
    "OO": "Difficultés à respirer ?",
    "OOO": "Pneumonie",
    "OON": "Grippe",
    "ON": "Douleur à la gorge ?",
    "ONO": "Angine bactérienne",
    "ONN": "Varicelle",
    "N": "Douleur localisée ?",
    "NO": "Douleur au ventre ?",
    "NOO": "Appendicite",
    "NON": "Douleur à la tête ?",
    "NONO": "Migraine sévère",
    "NONN": "Gastro-entérite",
    "NN": "Symptôme respiratoire ?",
    "NNO": "Asthme",
    "NNN": "Simple fatigue ou Stress intense"
}

# --- INTERFACE ---

if st.session_state.etape == "OFF":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    if st.button("🚀 ACTIVER LE SYSTÈME EXPERT"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    try: robot_place.image("tenor.gif", width=400)
    except: pass
    msg = "L'analyse est finie pour l'humain. Je vais maintenant générer une solution thérapeutique optimale."
    st.write(f"**Senku :** {msg}")
    parler(msg)
    if st.button("DÉMARRER L'ANALYSE"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    
    chemin = st.session_state.chemin
    question = ARBRE.get(chemin, "FIN")

    if "?" not in question:
        st.session_state.etape = "RESULTAT"
        st.rerun()
    else:
        st.info(f"🧬 Analyse binaire : {question}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ OUI"):
                st.session_state.chemin += "O"
                st.rerun()
        with col2:
            if st.button("❌ NON"):
                st.session_state.chemin += "N"
                st.rerun()

elif st.session_state.etape == "RESULTAT":
    try: robot_place.image("tenor.gif", width=400)
    except: pass
    
    maladie = ARBRE.get(st.session_state.chemin, "Inconnu")
    traitement = SOINS.get(maladie, "Repos et surveillance.")
    
    st.success(f"**Diagnostic : {maladie}**")
    parler(f"Diagnostic : {maladie}. Voici votre ordonnance automatique.")

    # --- AFFICHAGE DE L'ORDONNANCE ---
    st.markdown("""
    <style>
    .ordonnance {
        background-color: white;
        color: black;
        padding: 20px;
        border: 2px solid #000;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ordonnance">
        <h2 style="text-align:center;">ORDONNANCE NUMÉRIQUE</h2>
        <p><b>Praticien :</b> IA Méga Senku v3.0</p>
        <p><b>Date :</b> 16/03/2026</p>
        <hr>
        <p><b>Pathologie détectée :</b> {maladie}</p>
        <p><b>Traitement préconisé :</b></p>
        <p style="font-size: 18px;">- {traitement}</p>
        <br>
        <p style="text-align:right;"><i>Signature Numérique Certifiée</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 NOUVELLE ANALYSE"):
        st.session_state.etape = "OFF"
        st.session_state.chemin = ""
        st.rerun()
