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

if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.chemin = ""

st.markdown("# 👨‍🔬 Dr. Méga Senku - Intelligence Médicale")
st.markdown("### 🔍 Problématique : L'IA peut-elle surpasser le diagnostic humain ?")
st.divider()

robot_place = st.empty()

# --- BASE DE DONNÉES DES QUESTIONS (Arbre Profond) ---
ARBRE = {
    "": "Avez-vous de la fièvre ?",
    # Branche OUI (Fièvre)
    "O": "La fièvre est-elle apparue brutalement ?",
    "OO": "Dépasse-t-elle les 39.5°C ?",
    "OOO": "Ressentez-vous une raideur dans la nuque ?",
    "OOOO": "Avez-vous des taches violacées sur la peau ?",
    "OOOOO": "MÉNINGITE (Urgence Absolue)", # Diagnostic rapide si grave
    "OOON": "Avez-vous une toux avec des douleurs thoraciques ?",
    "OOONO": "Est-ce que vous crachez du sang ?",
    "OOONOO": "PNEUMONIE SÉVÈRE",
    "ON": "Est-ce une fièvre modérée avec fatigue ?",
    "ONO": "Avez-vous les ganglions du cou gonflés ?",
    "ONOO": "Est-ce que vous avez du mal à ouvrir la bouche ?",
    "ONOOO": "ANGINE BLANCHE",
    "ONON": "Avez-vous des courbatures généralisées ?",
    "ONONO": "GRIPPE SAISONNIÈRE",
    
    # Branche NON (Pas de fièvre)
    "N": "Ressentez-vous une douleur physique ?",
    "NO": "La douleur est-elle abdominale (ventre) ?",
    "NOO": "Est-ce situé en bas à droite ?",
    "NOOO": "La douleur augmente-t-elle quand vous sautez ou marchez ?",
    "NOOOO": "Avez-vous des nausées ?",
    "NOOOOO": "APPENDICITE",
    "NON": "La douleur est-elle dans la tête ?",
    "NONO": "Est-ce que la lumière vous est insupportable ?",
    "NONOO": "Est-ce accompagné de vomissements ?",
    "NONOOO": "MIGRAINE CHRONIQUE",
    "NN": "Est-ce un problème respiratoire ?",
    "NNO": "Entendez-vous un sifflement quand vous expirez ?",
    "NNOO": "Est-ce que cela empire la nuit ?",
    "NNOOO": "ASTHME",
    "NNN": "Est-ce une fatigue intense ?",
    "NNNO": "Avez-vous le teint très pâle ?",
    "NNNOO": "ANÉMIE SÉVÈRE",
    "NNNN": "Sentez-vous un stress psychologique important ?",
    "NNNNO": "BURN-OUT / ÉPUISEMENT"
}

# Questions de "Levée de doute" si le chemin est trop long
QUESTIONS_SUPPLEMENTAIRES = [
    "Ressentez-vous une accélération de votre rythme cardiaque ?",
    "Avez-vous des vertiges quand vous vous levez ?",
    "Vos symptômes sont-ils plus forts le matin ?",
    "Avez-vous pris un médicament qui n'a pas fonctionné ?",
    "Est-ce que cette douleur vous empêche de dormir ?",
    "Avez-vous voyagé récemment à l'étranger ?",
    "Y a-t-il des cas similaires dans votre entourage ?",
    "Ressentez-vous un engourdissement dans les membres ?",
    "Avez-vous une perte d'appétit totale ?",
    "L'IA a besoin d'une dernière confirmation : vos symptômes sont-ils stables ?"
]

# --- LOGIQUE ---

if st.session_state.etape == "OFF":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    if st.button("🚀 ACTIVER LE SCANNER MÉDICAL"):
        st.session_state.etape = "INTRO"
        st.rerun()

elif st.session_state.etape == "INTRO":
    try: robot_place.image("tenor.gif", width=400)
    except: pass
    msg = "L'humain s'arrête après 3 questions. Ma logique binaire va explorer chaque branche de votre système biologique. Scan complet activé."
    st.write(f"💬 **Senku :** {msg}")
    parler(msg)
    if st.button("DÉMARRER"):
        st.session_state.etape = "QUESTIONS"
        st.rerun()

elif st.session_state.etape == "QUESTIONS":
    try: robot_place.image("repos.jpg", width=400)
    except: pass
    
    chemin = st.session_state.chemin
    nb_questions = len(chemin)
    
    # 1. On cherche dans l'arbre principal
    sujet = ARBRE.get(chemin)
    
    # 2. Si on n'est pas encore à 10 questions, on force des questions supplémentaires
    if nb_questions < 10:
        if sujet and "?" in sujet:
            question_a_poser = sujet
        else:
            # Si l'arbre est fini mais qu'on a moins de 10 questions, on pioche dans les suppléments
            index_supp = nb_questions % len(QUESTIONS_SUPPLEMENTAIRES)
            question_a_poser = f"[Analyse de précision] {QUESTIONS_SUPPLEMENTAIRES[index_supp]}"
    else:
        # Après 10 questions, si on a un diagnostic (pas de point d'interrogation), on finit
        if sujet and "?" not in sujet:
            st.session_state.etape = "RESULTAT"
            st.rerun()
        else:
            # Sinon on continue un peu pour être sûr
            index_supp = nb_questions % len(QUESTIONS_SUPPLEMENTAIRES)
            question_a_poser = f"[Levée de doute finale] {QUESTIONS_SUPPLEMENTAIRES[index_supp]}"
            if nb_questions > 12: # Sécurité pour ne pas être infini non plus
                st.session_state.etape = "RESULTAT"
                st.rerun()

    st.write(f"📊 **Examen biologique n°{nb_questions + 1}**")
    st.progress(min(nb_questions * 10, 100))
    st.info(question_a_poser)
    
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
    
    # On cherche le dernier diagnostic connu dans le chemin
    diag = "Pathologie complexe (Nécessite Scanner)"
    for i in range(len(st.session_state.chemin), 0, -1):
        test_chemin = st.session_state.chemin[:i]
        if test_chemin in ARBRE and "?" not in ARBRE[test_chemin]:
            diag = ARBRE[test_chemin]
            break

    st.success(f"### Diagnostic final : {diag}")
    parler(f"Analyse terminée après {len(st.session_state.chemin)} tests. Résultat : {diag}.")

    st.markdown(f"""
    <div style="background-color: white; color: black; padding: 20px; border: 3px solid black;">
        <h2 style="text-align:center;">ORDONNANCE IA MÉGAVERSION</h2>
        <p><b>Diagnostic :</b> {diag}</p>
        <p><b>Niveau de scan :</b> {len(st.session_state.chemin)} étapes logiques</p>
        <hr>
        <p>👉 Repos strict et suivi des constantes vitales.</p>
        <p style="font-size:10px;">Généré par Dr. Méga Senku - IA de démonstration.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 REFAIRE UN SCAN"):
        st.session_state.etape = "OFF"
        st.session_state.chemin = ""
        st.rerun()
