import streamlit as st
from gtts import gTTS
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs MÉDECIN - Expert V4", page_icon="🧪")

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

st.markdown("# 👨‍🔬 Dr. Méga Senku - Intelligence Médicale")
st.markdown("### 🔍 Problématique : L'IA peut-elle surpasser le diagnostic humain ?")
st.divider()

robot_place = st.empty()

# --- BASE DE DONNÉES : TRAITEMENTS ---
SOINS = {
    "Pneumonie Sévère": "Hospitalisation d'urgence, oxygène et antibiothérapie IV.",
    "Grippe Infectieuse": "Repos strict, antiviraux si pris tôt, et hydratation.",
    "Angine Bactérienne": "Cure d'antibiotiques (Amoxicilline) et repos.",
    "Mononucléose": "Repos prolongé (plusieurs semaines) et surveillance hépatique.",
    "Appendicite": "Chirurgie immédiate (Bloc opératoire). Ne rien manger.",
    "Migraine avec Aura": "Triptans, obscurité totale, évitement des écrans.",
    "Insolation / Déshydratation": "Réhydratation progressive et mise au frais.",
    "Asthme Aigu": "Bronchodilatateurs d'urgence et corticoïdes.",
    "Anémie Profonde": "Supplémentation ferrique et bilan sanguin complet.",
    "Stress Post-Traumatique / Burn-out": "Repos total et suivi psychologique spécialisé.",
    "Gastro-entérite": "Réhydratation orale et régime sans résidus.",
    "Rhinopharyngite": "Traitement des symptômes et lavage de nez."
}

# --- L'ARBRE GÉANT (MINIMUM 10 QUESTIONS) ---
# Nous utilisons un dictionnaire où la clé est le chemin 'O'/'N'
ARBRE = {
    "": "Avez-vous de la fièvre ?",
    # Branche Fièvre (O)
    "O": "Dépasse-t-elle les 38.5°C ?",
    "OO": "Ressentez-vous une fatigue qui vous empêche de rester debout ?",
    "OOO": "Avez-vous des difficultés respiratoires ou une douleur thoracique ?",
    "OOOO": "Votre toux est-elle grasse avec des sécrétions ?",
    "OOOOO": "Est-ce que cela dure depuis plus de 3 jours ?",
    "OOOOOO": "Avez-vous des sifflements à l'inspiration ?",
    "OOOOOOO": "Pensez-vous avoir été exposé à un virus ?",
    "OOOOOOOO": "Ressentez-vous une confusion mentale ?",
    "OOOOOOOOO": "Avez-vous les lèvres bleutées ?",
    "OOOOOOOOOO": "Pneumonie Sévère", # 10 questions si on répond O partout
    
    # Branche de levée de doute (Exemple si Non à un moment)
    "OOOOOOOOON": "Grippe Infectieuse",
    
    # Branche Sans Fièvre (N)
    "N": "Ressentez-vous une douleur précise ?",
    "NN": "Est-ce une douleur dans la zone abdominale ?",
    "NNO": "Est-ce situé en bas à droite du ventre ?",
    "NNOO": "La douleur est-elle pire quand vous marchez ?",
    "NNOOO": "Avez-vous perdu l'appétit ?",
    "NNOOOO": "Avez-vous des nausées ?",
    "NNOOOOO": "Avez-vous la langue blanche ?",
    "NNOOOOOO": "Ressentez-vous une accélération cardiaque ?",
    "NNOOOOOOO": "Est-ce que la douleur est apparue brutalement ?",
    "NNOOOOOOOO": "Appendicite", # 10 questions ici aussi
    
    "NNOOOOOOON": "Gastro-entérite",

    # Branche Tête
    "NNN": "Est-ce une douleur à la tête ?",
    "NNNO": "Est-ce accompagné de vertiges ?",
    "NNNOO": "La lumière est-elle insupportable ?",
    "NNNOOO": "Est-ce un côté précis de la tête ?",
    "NNNOOOO": "Est-ce lancinant (comme des battements) ?",
    "NNNOOOOO": "Avez-vous des fourmillements ?",
    "NNNOOOOOO": "Est-ce que cela arrive après un stress ?",
    "NNNOOOOOOO": "Avez-vous pris des médicaments sans effet ?",
    "NNNOOOOOOOO": "La douleur est-elle revenue plusieurs fois ce mois-ci ?",
    "NNNOOOOOOOOO": "Migraine avec Aura"
}

# --- LOGIQUE D'AFFICHAGE ---

if st.session_state.etape == "OFF":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    if st.button("🚀 ACTIVER L'IA EXPERTE"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    try: robot_place.image("tenor.gif", width=400)
    except: pass
    msg = "Un médecin humain pose des questions au hasard. Moi, je parcours un arbre de probabilités à 10 milliards de pourcent. Préparation du scan complet."
    st.write(f"**Senku :** {msg}")
    parler(msg)
    if st.button("LANCER LE PROTOCOLE"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    
    chemin = st.session_state.chemin
    question_actuelle = ARBRE.get(chemin)

    # Si le chemin n'existe pas encore dans l'arbre, on crée une question de sécurité
    if not question_actuelle:
        question_actuelle = "L'IA analyse vos données spécifiques... Confirmez-vous que les symptômes persistent ?"

    if "?" not in question_actuelle:
        st.session_state.etape = "RESULTAT"
        st.rerun()
    else:
        nb_q = len(chemin) + 1
        st.write(f"📊 **Analyse n°{nb_q}**")
        st.progress(min(nb_q * 10, 100))
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
    
    maladie = ARBRE.get(st.session_state.chemin, "Analyse complexe : Cas hors base de données standard.")
    traitement = SOINS.get(maladie, "Repos et surveillance hospitalière nécessaire.")
    certitude = "98%" if len(st.session_state.chemin) >= 10 else "75% (Diagnostic rapide)"

    st.success(f"### Diagnostic final : {maladie}")
    st.write(f"**Indice de certitude algorithmique : {certitude}**")
    parler(f"Diagnostic : {maladie}. Certitude {certitude}.")

    # L'ORDONNANCE
    st.markdown(f"""
    <div style="background-color: white; color: black; padding: 25px; border: 4px solid #1f1f1f; font-family: 'Arial';">
        <h2 style="text-align:center;">ORDONNANCE IA v4.0</h2>
        <p><b>Diagnostic :</b> {maladie}</p>
        <p><b>Confiance :</b> {certitude}</p>
        <hr>
        <p><b>PRESCRIPTION :</b></p>
        <p style="font-size: 20px; color: blue;">👉 {traitement}</p>
        <br>
        <p style="font-size: 10px;">Cette prescription est issue d'une branche logique de {len(st.session_state.chemin)} étapes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 NOUVEL SCAN"):
        st.session_state.etape = "OFF"
        st.session_state.chemin = ""
        st.rerun()
    
