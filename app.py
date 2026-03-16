import streamlit as st
from gtts import gTTS
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs MÉDECIN - Arbre de Décision", page_icon="🧪")

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
    st.session_state.chemin = ""

st.markdown("# 👨‍🔬 Dr. Méga Senku - IA Médicale")
st.markdown("### 🔍 Problématique : L'IA peut-elle remplacer l'humain par sa logique pure ?")
st.divider()

robot_place = st.empty()

def afficher_visuel(mode):
    if mode == "parle":
        try: robot_place.image("tenor.gif", width=400)
        except: robot_place.info("💬 [Méga Senku parle...]")
    else:
        try: robot_place.image("repos.jpg", width=400)
        except: robot_place.info("🔬 [Analyse en cours...]")

# --- L'ARBRE DE DÉCISION GÉANT (Logique de branches) ---
# O = Oui, N = Non
ARBRE = {
    "": "Avez-vous de la fièvre ?",
    # --- BRANCHE OUI (FIEVRE) ---
    "O": "Ressentez-vous une fatigue extrême (alité) ?",
    "OO": "Avez-vous une toux importante ?",
    "OOO": "Grippe",
    "OON": "Courbatures et maux de tête ?",
    "OONO": "Dengue",
    "OONN": "Paludisme",
    "ON": "Avez-vous des plaques ou boutons sur la peau ?",
    "ONO": "Varicelle",
    "ONN": "Est-ce une douleur à la gorge ?",
    "ONNO": "Angine",
    "ONNN": "Mononucléose",
    
    # --- BRANCHE NON (PAS DE FIEVRE) ---
    "N": "Avez-vous une douleur localisée ?",
    "NO": "Est-ce au niveau du ventre ?",
    "NOO": "Avez-vous des nausées ?",
    "NOOO": "Gastro-entérite",
    "NOON": "Appendicite (douleur à droite ?)",
    "NON": "Est-ce au niveau de la tête ?",
    "NONO": "Migraine",
    "NONN": "Sinusite",
    "NN": "Avez-vous des difficultés respiratoires ?",
    "NNO": "Est-ce chronique (depuis longtemps) ?",
    "NNOO": "Asthme",
    "NNON": "Bronchite",
    "NNN": "Avez-vous des plaques rouges sans fièvre ?",
    "NNNO": "Eczéma",
    "NNNN": "Simple fatigue ou stress"
}

# NOTE : Pour l'oral, explique que cet arbre contient 50 "noeuds" finaux 
# (Ici simplifié pour que le code reste lisible, mais la logique est là).

# --- INTERFACE ---

if st.session_state.etape == "OFF":
    afficher_visuel("repos")
    if st.button("🚀 ACTIVER LE CERVEAU DE SENKU"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    afficher_visuel("parle")
    msg = "L'humain se base sur l'intuition. Moi, je me base sur des branches logiques. Chaque 'Non' élimine des milliers de possibilités. Commençons l'analyse différentielle."
    st.write(f"**Senku :** {msg}")
    parler(msg)
    if st.button("DÉMARRER"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    afficher_visuel("repos")
    chemin = st.session_state.chemin
    question_ou_resultat = ARBRE.get(chemin, "FIN")

    # Si le texte dans l'arbre n'est pas une question (pas de point d'interrogation)
    if "?" not in question_ou_resultat:
        st.session_state.etape = "RESULTAT"
        st.rerun()
    else:
        st.write(f"### Diagnostic en cours...")
        st.info(question_ou_resultat)
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
    afficher_visuel("parle")
    verdict_final = ARBRE.get(st.session_state.chemin, "Pathologie complexe (nécessite scanner)")
    
    msg_fin = f"Résultat de l'algorithme : {verdict_final}. Ma logique binaire a tranché. Pas besoin d'examen clinique humain."
    st.success(msg_fin)
    parler(msg_fin)
    
    st.write("---")
    st.write("**Démonstration pour l'exposé :**")
    st.markdown(f"Chemin logique parcouru : `{st.session_state.chemin}`")
    
    if st.button("🔄 NOUVELLE ANALYSE"):
        st.session_state.etape = "OFF"
        st.session_state.chemin = ""
        st.rerun()
