# --- Programme de Diagnostic Médical par IA (Simulation) ---

# Base de données simplifiée de 50 maladies et leurs symptômes signatures
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
"Pneumonie": ["toux avec sécrétions colorées", "douleur thoracique profonde", "fièvre"],
"Appendicite": ["douleur aiguë à droite du ventre", "nausées", "ventre dur"],
"Rougeole": ["taches blanches dans la bouche", "éruption cutanée", "forte fièvre"],
"Mononucléose": ["ganglions gonflés", "immense fatigue", "mal de gorge"],
"Cholestérol": ["souvent aucun symptôme (détecté par prise de sang)"],
"Hypertension": ["maux de tête matinaux", "bourdonnements d'oreilles", "vertiges"],
"Insolation": ["peau brûlante et sèche", "confusion", "maux de tête après exposition"],
"Mélanome": ["grain de beauté qui change de couleur ou de forme"],
"Eczéma": ["plaques rouges sèches", "fortes démangeaisons"],
"Sinusite": ["douleur sous les yeux", "pression au visage", "nez bouché"],
"Scarlatine": ["langue rouge framboise", "éruption cutanée granuleuse"],
"Rage": ["peur de l'eau", "agitation extrême", "salivation excessive"],
"Tétanos": ["mâchoire contractée", "spasmes musculaires", "difficulté à avaler"],
"Paludisme": ["pics de fièvre tous les deux jours", "sueurs froides"],
"Dengue": ["douleur derrière les yeux", "éruption cutanée", "douleurs articulaires"],
"Maladie de Lyme": ["tache rouge en forme de cible", "morsure de tique", "fatigue"],
"Cystite": ["envie d'uriner constante", "pesanteur dans le bassin"],
"Urticaire": ["plaques gonflées comme des piqûres d'orties"],
"Calculs rénaux": ["douleur brutale et intense dans le dos", "agitation"],
"Goutte": ["gros orteil rouge, gonflé et très douloureux"],
"Hernie discale": ["douleur qui descend dans la jambe (sciatique)", "fourmillements"],
"Hypothyroïdie": ["frilosité", "prise de poids inexpliquée", "ralentissement du rythme"],
"Hyperthyroïdie": ["palpitations", "yeux exorbités", "perte de poids"],
"Insuffisance cardiaque": ["chevilles gonflées", "essoufflement à l'effort"],
"Psoriasis": ["plaques avec squames blanches (peaux mortes)", "coudes/genoux"],
"Gale": ["petits sillons sous la peau", "démangeaisons nocturnes intenses"],
"Pharyngite": ["fond de la gorge très inflammé", "ganglions"],
"Coqueluche": ["quintes de toux qui finissent par un bruit de chant de coq"],
"Oreillons": ["gonflement des joues (parotides)", "douleur en mâchant"],
"Zona": ["éruption douloureuse suivant le trajet d'un nerf"],
"Apnée du sommeil": ["ronflements bruyants", "arrêts respiratoires la nuit", "somnolence"],
"Choc anaphylactique": ["gonflement rapide du visage", "difficulté à respirer (urgence)"],
"Ulcère": ["brûlure d'estomac calmée par les repas"],
"Maladie de Crohn": ["diarrhées chroniques", "douleurs au ventre", "perte de poids"],
"Méningite": ["nuque raide", "peur de la lumière", "taches violettes sur la peau"]
}

# Fonction de diagnostic
def analyser_symptomes(symptome_utilisateur):
print(f"\n--- Analyse de l'IA pour : '{symptome_utilisateur}' ---")
trouve = False

for maladie, symptomes in maladies_data.items():
if symptome_utilisateur.lower() in [s.lower() for s in symptomes]:
print(f"ALERTE : Diagnostic possible -> {maladie}")
print(f"Symptômes associés : {', '.join(symptomes)}")
trouve = True

if not trouve:
print("Aucune correspondance exacte trouvée. Consultez un médecin.")

# Test du programme
print("Bienvenue dans le simulateur de Nanomédecine IA")
saisie = input("Entrez un symptôme (ex: nuque raide, soif excessive) : ")
analyser_symptomes(saisie)
