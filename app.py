import streamlit as st
import time

# --- CONFIGURATION ---
NOM_IA = "Dr. IA"

# --- IMAGE ---
st.image("robot_diagnostic.jpg", width=300)

st.title(f"🤖 {NOM_IA} : Diagnostic Intelligent")

# --- BASE DE DONNÉES ---
maladies_data = {
"Angine": ["gorge rouge", "difficulté à avaler", "fièvre"],
"Grippe": ["courbatures", "forte fièvre", "frissons"],
"Diabète type 1": ["soif excessive", "envie fréquente d'uriner", "fatigue intense"],
"Asthme": ["sifflement respiratoire", "essoufflement", "toux sèche"],
"Varicelle": ["boutons rouges avec démangeaisons", "fièvre légère"],
"Otite": ["douleur à l'oreille", "perte d'audition temporaire"],
"Gastro-entérite": ["nausées", "douleurs abdominales", "déshydratation"],
"Anémie": ["pâleur extrême", "essoufflement rapide", "étourdissements"],
"Conjonctivite": ["œil rouge", "écoulement purulent", "paupières collées"],
"Allergie au pollen": ["éternuements en salve", "nez qui coule", "yeux qui piquent"],
"Bronchite": ["toux grasse", "douleur au thorax", "fatigue"],
"Rhinopharyngite": ["nez bouché", "mal de gorge léger", "éternuements"],
"Laryngite": ["voix enrouée ou cassée", "toux aboyante"],
"Infection urinaire": ["brûlure en urinant", "besoin pressant", "douleur bas-ventre"],
"Migraine": ["douleur d'un seul côté de la tête", "sensibilité à la lumière"],
"Pneumonie": ["toux avec sécrétions colorées", "douleur thoracique profonde"],
"Appendicite": ["douleur aiguë à droite du ventre", "nausées", "ventre dur"],
"Rougeole": ["taches blanches dans la bouche", "éruption cutanée", "forte fièvre"],
"Mononucléose": ["ganglions gonflés", "immense fatigue", "mal de gorge"],
"Cholestérol": ["excès de lipides", "fatigue", "douleurs jambes"],
"Hypertension": ["maux de tête matinaux", "bourdonnements d'oreilles", "vertiges"],
"Insolation": ["peau brûlante et sèche", "confusion", "maux de tête"],
"Mélanome": ["grain de beauté qui change de couleur", "asymétrie grain de beauté"],
"Eczéma": ["plaques rouges sèches", "fortes démangeaisons"],
"Sinusite": ["douleur sous les yeux", "pression au visage", "nez bouché"],
"Scarlatine": ["langue rouge framboise", "éruption cutanée granuleuse"],
"Rage": ["peur de l'eau", "agitation extrême", "salivation excessive"],
"Tétanos": ["mâchoire contractée", "spasmes musculaires", "difficulté à avaler"],
"Paludisme": ["pics de fièvre tous les deux jours", "sueurs froides"],
"Dengue": ["douleur derrière les yeux", "douleurs articulaires"],
"Maladie de Lyme": ["tache rouge en forme de cible", "morsure de tique"],
"Cystite": ["envie d'uriner constante", "pesanteur dans le bassin"],
"Urticaire": ["plaques gonflées comme des piqûres d'orties"],
"Calculs rénaux": ["douleur brutale et intense dans le dos", "agitation"],
"Goutte": ["gros orteil rouge et gonflé", "douleur nocturne orteil"],
"Hernie discale": ["douleur qui descend dans la jambe", "fourmillements"],
"Hypothyroïdie": ["frilosité", "prise de poids inexpliquée"],
"Hyperthyroïdie": ["palpitations", "yeux exorbités", "nervosité"],
"Insuffisance cardiaque": ["chevilles gonflées", "essoufflement à l'effort"],
"Psoriasis": ["plaques avec peaux mortes blanches", "coudes ou genoux"],
"Gale": ["petits sillons sous la peau", "démangeaisons nocturnes"],
"Pharyngite": ["fond de la gorge inflammé", "ganglions cou"],
"Coqueluche": ["quintes de toux bruyantes", "chant du coq"],
"Oreillons": ["gonflement des joues", "douleur en mâchant"],
"Zona": ["éruption douloureuse sur un nerf", "brûlure cutanée"],
"Apnée du sommeil": ["ronflements bruyants", "arrêts respiratoires la nuit"],
"Choc anaphylactique": ["gonflement rapide du visage", "difficulté à respirer"],
"Ulcère": ["brûlure d'estomac", "douleur après repas"],
"Maladie de Crohn": ["diarrhées chroniques", "douleurs ventre", "amaigrissement"],
"Méningite": ["nuque raide", "peur de la lumière", "taches violettes"]
}

# --- LOGIQUE ---
user_input = st.text_input("Posez votre question ici :")

if user_input:
st.write("Analyse en cours...")
time.sleep(1)

s_user = user_input.lower()
trouve = False

for maladie, symptomes in maladies_data.items():
if any(s.lower() in s_user for s in symptomes):
st.success(f"Diagnostic : **{maladie.upper()}**")
st.info(f"Symptômes signatures : {', '.join(symptomes)}")
st.warning("⚠️ Consultez un médecin pour confirmer.")
trouve = True
break

if not trouve:
st.error("Aucune correspondance trouvée dans ma base de données.")
