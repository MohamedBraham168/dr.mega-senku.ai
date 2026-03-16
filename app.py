import streamlit as st
from gtts import gTTS
import base64
import time
import qrcode
from io import BytesIO

# --- CONFIGURATION ---
st.set_page_config(page_title="IA vs MÉDECIN - Dr. Méga Senku", page_icon="🧪", layout="wide")

# Fonction de lecture vocale (gTTS)
def parler(texte):
    try:
        tts = gTTS(text=texte, lang='fr')
        # On utilise BytesIO pour ne pas créer de fichier sur le serveur
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# Initialisation des états
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.reponses = {}
    st.session_state.index_q = 0
    st.session_state.phrase_senku = ""

st.markdown("# 👨‍🔬 Dr. Méga Senku - Intelligence Médicale Avancée")
st.markdown("### 🔍 Problématique : L'IA peut-elle surpasser le diagnostic humain ?")
st.divider()

col_visuel, col_info = st.columns([1, 2])

# --- VISUEL ---
with col_visuel:
    robot_place = st.empty()
    try:
        if st.session_state.etape == "QUESTIONS":
            robot_place.image("repos.jpg", width=400)
        else:
            robot_place.image("tenor.gif", width=400)
    except:
        pass

# --- LOGIQUE ET TEXTE ---
with col_info:
    # --- LISTE DES 30 SYMPTÔMES (Base V7) ---
    QUESTIONS = [
        ("fievre", "Fièvre (>38.5°C) ?"), ("fatigue", "Fatigue intense / Épuisement ?"), ("frissons", "Frissons ou sueurs nocturnes ?"),
        ("tete", "Maux de tête violents ?"), ("gorge", "Mal de gorge intense ?"), ("nuque", "Raideur de la nuque ?"),
        ("vertiges", "Vertiges ou pertes d'équilibre ?"), ("ganglions", "Ganglions gonflés ?"),
        ("toux_seche", "Toux sèche irritante ?"), ("toux_grasse", "Toux avec sécrétions ?"), ("souffle", "Difficulté à respirer ?"),
        ("sifflement", "Sifflement respiratoire ?"), ("nez_coule", "Écoulement nasal ?"),
        ("nausees", "Nausées ?"), ("vomis", "Vomissements ?"), ("douleur_ventre", "Douleurs abdominales ?"),
        ("diarrhee", "Diarrhée ?"), ("appetit", "Perte d'appétit ?"),
        ("courbatures", "Douleurs musculaires ?"), ("dos", "Douleur vive dans le dos ?"), ("articulations", "Douleurs aux articulations ?"),
        ("boutons", "Apparition de boutons ?"), ("plaques", "Plaques rouges ?"), ("teint", "Teint pâle ou yeux jaunes ?"),
        ("perte_gout", "Perte du goût ou de l'odorat ?"), ("taches_bouche", "Taches blanches dans la bouche ?"),
        ("douleur_droite", "Douleur précise en bas à droite du ventre ?"), ("photophobie", "La lumière fait-elle mal ?"),
        ("soif", "Soif permanente ?"), ("oppression", "Oppression thoracique ?")
    ]

    # --- BASE DE DONNÉES (Base V7) ---
    DB = {
        "Grippe Infectieuse": (["fievre", "fatigue", "frissons", "toux_seche"], ["courbatures", "tete"], "Repos, Paracétamol, Hydratation."),
        "Méningite": (["fievre", "tete", "nausees", "vomis"], ["nuque", "photophobie"], "URGENCE VITALE : Appelez le 15."),
        "Appendicite Aiguë": (["fievre", "nausees", "vomis", "appetit"], ["douleur_ventre", "douleur_droite"], "URGENCE : Chirurgie."),
        "COVID-19": (["fievre", "toux_seche", "fatigue", "nez_coule"], ["perte_gout", "souffle"], "Isolement, Test PCR."),
        "Gastro-entérite": (["fatigue", "appetit", "douleur_ventre", "frissons"], ["vomis", "diarrhee"], "Solution réhydratation, Régime."),
        "Asthme Sévère": (["toux_seche", "oppression", "fatigue", "frissons"], ["souffle", "sifflement"], "Ventoline, Corticoïdes."),
        "Pneumonie": (["fievre", "frissons", "fatigue", "souffle"], ["toux_grasse", "oppression"], "Antibiotiques, Radio pulmonaire.")
    }

    # --- AFFICHAGE ---
    if st.session_state.etape == "OFF":
        st.session_state.phrase_senku = "Le diagnostic humain est lent. Ma logique binaire est instantanée. Scannons 30 points de données à 10 milliards de pourcent !"
        st.write(f"💬 **Senku :** {st.session_state.phrase_senku}")
        parler(st.session_state.phrase_senku)

        # GÉNÉRATION DU CODE QR
        url = "https://drmega-senkuai-27cruqmreat3uqpqgyt4ez.streamlit.app/" # Ton URL
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # Affichage du code QR
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Flashez pour tester sur mobile", width=200)

        if st.button("🚀 ACTIVER LE SCANNER (30 POINTS)"):
            st.session_state.etape = "QUESTIONS"
            st.rerun()

    elif st.session_state.etape == "QUESTIONS":
        idx = st.session_state.index_q
        if idx < len(QUESTIONS):
            id_s, txt = QUESTIONS[idx]
            st.write(f"📊 **Examen n°{idx+1} / 30**")
            st.progress((idx + 1) / len(QUESTIONS))
            st.info(txt)
            
            # Phrase de Senku selon la réponse (Optionnel, peut ralentir)
            if idx > 0:
                if st.session_state.reponses.get(QUESTIONS[idx-1][0]):
                    st.caption("🔬 *Intéressant... Donnée enregistrée.*")
                else:
                    st.caption("🔬 *Négatif. Poursuite du scan.*")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ OUI"):
                    st.session_state.reponses[id_s] = True
                    st.session_state.index_q += 1
                    st.rerun()
            with c2:
                if st.button("❌ NON"):
                    st.session_state.reponses[id_s] = False
                    st.session_state.index_q += 1
                    st.rerun()
        else:
            st.session_state.etape = "AI_THINKING"
            st.rerun()

    elif st.session_state.etape == "AI_THINKING":
        st.session_state.phrase_senku = "Analyse différentielle des 30 points de contrôle. Comparaison avec la matrice de 50 pathologies. Connexion neuronale établie."
        st.write(f"🔬 **Senku :** {st.session_state.phrase_senku}")
        parler(st.session_state.phrase_senku)
        
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.04)
            bar.progress(i + 1)
        st.session_state.etape = "RESULTAT"
        st.rerun()

    elif st.session_state.etape == "RESULTAT":
        mes_s = [k for k, v in st.session_state.reponses.items() if v]
        
        best_m = "Indéterminé (Symptômes trop vagues)"
        max_score = 0
        final_soin = "Veuillez consulter un médecin pour un examen clinique."

        for nom, (communs, signatures, soin) in DB.items():
            score_c = len(set(mes_s) & set(communs))
            score_s = len(set(mes_s) & set(signatures)) * 2 # Signatures double score
            total = score_c + score_s
            
            if total > max_score:
                max_score = total
                best_m = nom
                final_soin = soin

        # Phrase de fin
        if best_m == "Indéterminé":
            st.session_state.phrase_senku = "Analyse complexe. Vos symptômes ne correspondent à aucune matrice connue. L'examen humain est requis."
        else:
            st.session_state.phrase_senku = f"Diagnostic établi. Probabilité de {best_m}. Ma prescription est sans appel."

        st.success(f"### Résultat : {best_m}")
        st.write(f"💬 **Senku :** {st.session_state.phrase_senku}")
        parler(st.session_state.phrase_senku)

        # RAPPORT
        st.markdown(f"""
        <div style="background-color: white; color: black; padding: 25px; border: 5px solid #1f1f1f; border-radius: 15px;">
            <h2 style="text-align:center;">RAPPORT DE DIAGNOSTIC IA</h2>
            <p><b>Points analysés :</b> 30 symptômes</p>
            <p><b>Score de confiance :</b> {min(max_score * 10, 100)}%</p>
            <hr>
            <p><b>PATHOLOGIE :</b> {best_m}</p>
            <p><b>CONDUITE À TENIR :</b> {final_soin}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 NOUVELLE ANALYSE"):
            st.session_state.etape = "OFF"
            st.session_state.index_q = 0
            st.session_state.reponses = {}
            st.rerun()
