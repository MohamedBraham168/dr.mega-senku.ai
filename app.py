import time
import sys

# --- 1. CONFIGURATION DU ROBOT ---
# Pour ton site ou ton dossier, l'image est nommée : robot_diagnostic.jpg
NOM_IA = "Nano-Diagnostic V1.0"

def animation_chargement():
print(f"--- Connexion au {NOM_IA} ---")
barre = ["[□□□□□□□□□□]", "[■□□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■■■]"]
for etape in barre:
sys.stdout.write(f"\rInitialisation du système : {etape}")
sys.stdout.flush()
time.sleep(0.3)
print("\nSystème prêt. Analyseur de symptômes activé.\n")

# --- 2. BASE DE DONNÉES (50 MALADIES & SYMPTÔMES SIGNATURES) ---
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

# --- 3. LOGIQUE DE DIAGNOSTIC ---
def lancer_diagnostic():
animation_chargement()

print(f"--- {NOM_IA} à votre écoute ---")
symptome_saisi = input("Veuillez entrer le symptôme observé : ").lower()

trouve = False
print("\nRecherche dans la base de données génétiques...")
time.sleep(1)

for maladie, symptomes in maladies_data.items():
if symptome_saisi in [s.lower() for s in symptomes]:
print(f"\n[ALERTE] Correspondance trouvée : {maladie.upper()}")
print(f"Symptômes signatures détectés : {', '.join(symptomes)}")
print("-" * 40)
print("CONSEIL IA : Contactez un médecin pour confirmer ce diagnostic.")
trouve = True
break # On s'arrête dès qu'on trouve la maladie signature

if not trouve:
print("\nAucune signature exacte trouvée dans la base de données.")
print("L'IA nécessite plus d'analyses ou une intervention humaine.")

# --- LANCEMENT ---
if __name__ == "__main__":
lancer_diagnostic()
