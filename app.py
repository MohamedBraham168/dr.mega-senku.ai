import streamlit as st
from gtts import gTTS
import base64

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

if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.chemin = ""

st.markdown("# 👨‍🔬 Dr. Méga Senku - Système Expert")
st.markdown("### 🔍 Problématique : L'IA peut-elle surpasser le diagnostic humain ?")
st.divider()

robot_place = st.empty()

# --- L'ARBRE DE DÉCISION GÉANT ---
# O = Oui, N = Non
ARBRE = {
    "": "Avez-vous de la fièvre ?",
    # Branche FIEVRE
    "O": "La fièvre est-elle supérieure à 39°C ?",
    "OO": "Avez-vous des difficultés à respirer ?",
    "OOO": "Pneumonie",
    "OON": "Avez-vous une toux sèche et des courbatures ?",
    "OONO": "Grippe",
    "OONN": "Bronchite aiguë",
    "ON": "Avez-vous des plaques rouges sur le corps ?",
    "ONO": "Avez-vous eu un contact avec un enfant malade ?",
    "ONOO": "Varicelle",
    "ONON": "Rougeole",
    "ONN": "Avez-vous très mal à la gorge ?",
    "ONNO": "Angine bactérienne",
    "ONNN": "Mononucléose",
    # Branche SANS FIEVRE
    "N": "Ressentez-vous une douleur physique localisée ?",
    "NO": "La douleur est-elle située dans l'abdomen ?",
    "NOO": "La douleur est-elle en bas à droite du ventre ?",
    "NOOO": "Appendicite",
    "NOON": "Est-ce lié à ce que vous avez mangé ?",
    "NOONO": "Intoxication alimentaire",
    "NOONN": "Gastro-entérite",
    "NON": "La douleur est-elle située à la tête ?",
    "NONO": "La lumière vous fait-elle mal aux yeux ?",
    "NONOO": "Migraine sévère",
    "NONON": "Céphalée de tension",
    "NONN": "Est-ce une douleur articulaire ?",
    "NONNO": "Arthrose",
    "NONNN": "Sciatique",
    "NN": "Avez-vous un symptôme respiratoire (toux, sifflement) ?",
    "NNO": "Est-ce que cela arrive souvent (chronique) ?",
    "NNOO": "Asthme",
    "NNON": "Allergie saisonnière",
    "NNN": "Est-ce une fatigue inhabituelle ?",
    "NNNO": "Anémie (manque de fer)",
    "NNNN": "Simple fatigue ou Stress intense"
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
    msg = "L'humain oublie des détails. Ma base de données, non. Je vais scanner vos symptômes à travers mon arbre logique."
    st.write(f"**Senku :** {msg}")
    parler(msg)
    if st.button("DÉMARRER L'ANALYSE"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    
    chemin = st.session_state.chemin
    question_actuelle = ARBRE.get(chemin, "FIN")

    # Si c'est un résultat final (pas de point d'interrogation)
    if "?" not in question_actuelle:
        st.session_state.etape = "RESULTAT"
        st.rerun()
    else:
        # Barre de progression
        progression = len(chemin) * 20
        st.progress(min(progression, 100))
        
        st.write(f"### Question de l'IA :")
        st.info(question_actuelle)
        
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
    
    maladie = ARBRE.get(st.session_state.chemin, "Pathologie non répertoriée")
    verdict = f"Diagnostic établi : {maladie}. La logique binaire a parlé. L'IA a fini son travail."
    
    st.success(verdict)
    parler(verdict)
    
    st.write("---")
    st.write(f"**Analyse du chemin logique :** `{st.session_state.chemin}`")
    st.caption("Chaque lettre correspond à un embranchement de l'arbre décisionnel médical.")

    if st.button("🔄 NOUVEAU PATIENT"):
        st.session_state.etape = "OFF"
        st.session_state.chemin = ""
        st.rerun()
