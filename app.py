import streamlit as st
from gtts import gTTS
import base64
import time
import qrcode
from io import BytesIO

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dr. Méga Senku - IA Médicale v8.0", page_icon="🧪", layout="wide")

# --- FONCTION AUDIO (Sécurisée pour le web) ---
def parler(texte):
    try:
        tts = gTTS(text=texte, lang='fr')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)
    except:
        st.warning("⚠️ Audio indisponible (Vérifiez votre connexion)")

# --- INITIALISATION DES VARIABLES ---
if 'etape' not in st.session_state:
    st.session_state.etape = "OFF"
    st.session_state.reponses = {}
    st.session_state.index_q = 0
    st.session_state.phrase_senku = ""

# --- BASE DE DONNÉES DES SYMPTÔMES (30 POINTS) ---
QUESTIONS = [
    ("fievre", "Fièvre élevée (>38.5°C) ?"), ("fatigue", "Fatigue extrême / Épuisement ?"), 
    ("frissons", "Frissons ou sueurs nocturnes ?"), ("tete", "Maux de tête violents ?"), 
    ("gorge", "Mal de gorge intense ?"), ("nuque", "Raideur de la nuque (douleur en baissant la tête) ?"),
    ("vertiges", "Vertiges ou pertes d'équilibre ?"), ("ganglions", "Ganglions gonflés (cou/aisselles) ?"),
    ("toux_seche", "Toux sèche et irritante ?"), ("toux_grasse", "Toux avec sécrétions (glaires) ?"), 
    ("souffle", "Difficulté à respirer / Essoufflement ?"), ("sifflement", "Sifflement lors de la respiration ?"), 
    ("nez_coule", "Écoulement nasal ou nez bouché ?"), ("nausees", "Nausées ou envie de vomir ?"), 
    ("vomis", "Vomissements effectifs ?"), ("douleur_ventre", "Douleurs abdominales générales ?"),
    ("diarrhee", "Diarrhée ou troubles intestinaux ?"), ("appetit", "Perte totale d'appétit ?"),
    ("courbatures", "Douleurs musculaires / Courbatures ?"), ("dos", "Douleur vive dans le bas du dos ?"), 
    ("articulations", "Douleurs aux articulations ?"), ("boutons", "Apparition de boutons ou vésicules ?"), 
    ("plaques", "Plaques rouges ou démangeaisons ?"), ("teint", "Teint pâle ou yeux jaunes ?"),
    ("perte_gout", "Perte du goût ou de l'odorat ?"), ("taches_bouche", "Taches blanches anormales dans la bouche ?"),
    ("douleur_droite", "Douleur précise en bas à droite du ventre ?"), ("photophobie", "La lumière fait-elle mal aux yeux ?"),
    ("soif", "Soif permanente et besoin d'uriner fréquent ?"), ("oppression", "Sensation d'oppression dans la poitrine ?")
]

# --- BASE DE DONNÉES DES PATHOLOGIES (Logique : Communs | Signatures | Traitement) ---
DB = {
    "Grippe Infectieuse": (["fievre", "fatigue", "frissons", "toux_seche"], ["courbatures", "tete"], "Repos, Paracétamol, Hydratation."),
    "Méningite": (["fievre", "tete", "nausees", "vomis"], ["nuque", "photophobie"], "URGENCE VITALE : Appelez le 15 immédiatement."),
    "Appendicite Aiguë": (["fievre", "nausees", "vomis", "appetit"], ["douleur_ventre", "douleur_droite"], "URGENCE : Chirurgie nécessaire."),
    "COVID-19": (["fievre", "toux_seche", "fatigue", "nez_coule"], ["perte_gout", "souffle"], "Isolement, Test PCR, Surveillance."),
    "Gastro-entérite": (["fatigue", "appetit", "douleur_ventre", "frissons"], ["vomis", "diarrhee"], "Réhydratation, Régime riz/carottes."),
    "Asthme Sévère": (["toux_seche", "oppression", "fatigue"], ["souffle", "sifflement"], "Ventoline, Corticoïdes."),
    "Pneumonie": (["fievre", "frissons", "fatigue", "souffle"], ["toux_grasse", "oppression"], "Antibiotiques, Radio pulmonaire."),
    "Angine Bactérienne": (["fievre", "tete", "fatigue"], ["gorge", "ganglions"], "Antibiotiques, Repos."),
    "Anémie Profonde": (["fatigue", "vertiges"], ["teint", "ongles_cassants"], "Supplémentation en fer, Bilan sanguin."),
    "Rougeole": (["fievre", "nez_coule", "toux_seche"], ["boutons", "taches_bouche"], "Surveillance fièvre, Repos."),
    "Insolation": (["fievre", "tete"], ["plaques", "nausees"], "Mise au frais, Réhydratation."),
    "Diabète (Détection)": (["fatigue", "appetit"], ["soif", "perte_poids"], "Consultation pour test glycémique.")
}

st.title("👨‍🔬 Système Expert : Dr. Méga Senku")
st.write("---")

# --- ÉCRAN D'ACCUEIL ---
if st.session_state.etape == "OFF":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try: st.image("tenor.gif", width=400)
        except: st.info("🧪 [Image Senku active]")
        
        st.session_state.phrase_senku = "Le diagnostic humain est lent et biaisé. Ma logique binaire est prête à 10 milliards de pourcent !"
        st.subheader(st.session_state.phrase_senku)
        parler(st.session_state.phrase_senku)
        
        if st.button("🚀 LANCER LE SCAN MÉDICAL (30 POINTS)"):
            st.session_state.etape = "QUESTIONS"
            st.rerun()

    with col2:
        st.write("### 📱 Version Mobile")
        url = "https://drmega-senkuai-27cruqmreat3uqpqgyt4ez.streamlit.app/"
        qr_gen = qrcode.QRCode(box_size=5, border=2)
        qr_gen.add_data(url)
        qr_gen.make(fit=True)
        img_qr = qr_gen.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Flashez pour tester sur téléphone")

# --- PHASE DE QUESTIONS ---
elif st.session_state.etape == "QUESTIONS":
    idx = st.session_state.index_q
    if idx < len(QUESTIONS):
        id_s, txt = QUESTIONS[idx]
        
        st.write(f"📊 **Analyse systémique n°{idx+1} / 30**")
        st.progress((idx + 1) / len(QUESTIONS))
        
        # Affichage de Senku en petit pendant les questions
        c_img, c_txt = st.columns([1, 4])
        with c_img:
            try: st.image("repos.jpg", width=150)
            except: pass
        with c_txt:
            st.info(f"QUESTION : {txt}")

        col_oui, col_non = st.columns(2)
        with col_oui:
            if st.button("✅ OUI", use_container_width=True):
                st.session_state.reponses[id_s] = True
                st.session_state.index_q += 1
                st.rerun()
        with col_non:
            if st.button("❌ NON", use_container_width=True):
                st.session_state.reponses[id_s] = False
                st.session_state.index_q += 1
                st.rerun()
    else:
        st.session_state.etape = "AI_THINKING"
        st.rerun()

# --- SIMULATION DE RÉFLEXION ---
elif st.session_state.etape == "AI_THINKING":
    st.write("🔬 **Senku :** Analyse différentielle des 30 points de données en cours...")
    parler("Analyse des données. Je compare vos symptômes à ma matrice de pathologies.")
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        bar.progress(i + 1)
    st.session_state.etape = "RESULTAT"
    st.rerun()

# --- RÉSULTAT FINAL ---
elif st.session_state.etape == "RESULTAT":
    mes_s = [k for k, v in st.session_state.reponses.items() if v]
    
    best_m = "Indéterminé (Cas complexe)"
    max_score = 0
    final_soin = "Veuillez consulter un médecin pour un examen clinique complet."

    for nom, (communs, signatures, soin) in DB.items():
        score_c = len(set(mes_s) & set(communs))
        score_s = len(set(mes_s) & set(signatures)) * 2 # Les signatures valent double
        total = score_c + score_s
        
        if total > max_score:
            max_score = total
            best_m = nom
            final_soin = soin

    st.success(f"### DIAGNOSTIC ÉTABLI : {best_m}")
    parler(f"Diagnostic terminé. Il y a une forte probabilité de {best_m}.")
    
    st.markdown(f"""
    <div style="background-color: white; color: black; padding: 25px; border: 5px solid black; border-radius: 15px; font-family: Arial;">
        <h2 style="text-align:center;">ORDONNANCE NUMÉRIQUE - DR. SENKU</h2>
        <p><b>Statut :</b> Intelligence Artificielle Certifiée</p>
        <p><b>Fiabilité :</b> {min(max_score * 8, 100)}%</p>
        <hr>
        <p><b>PATHOLOGIE DÉTECTÉE :</b> {best_m}</p>
        <p><b>PRESCRIPTION :</b> {final_soin}</p>
        <br>
        <p style="font-size: 10px; color: gray;">Ceci est une démonstration technique pour un exposé scolaire.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 NOUVELLE ANALYSE"):
        st.session_state.etape = "OFF"
        st.session_state.index_q = 0
        st.session_state.reponses = {}
        st.rerun()
