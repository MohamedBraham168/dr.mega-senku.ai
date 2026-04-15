import streamlit as st
# 1. CONFIGURATION DE LA PAGE (Pour un look pro)
st.set_page_config(page_title="Assistant Diagnostic Médical", page_icon="⚕️")

# 2. BASE DE DONNÉES DES MALADIES
maladies_data = {
"Angine": ["mal de gorge", "fièvre", "difficulté à avaler"],
"Grippe": ["fièvre", "courbatures", "toux sèche", "fatigue"],
"Diabète": ["soif excessive", "envie fréquente d'uriner", "fatigue", "vision floue"],
"Asthme": ["essoufflement", "sifflement respiratoire", "oppression thoracique"],
"Méningite": ["forte fièvre", "maux de tête violents", "nuque raide", "vomissements"],
"Gastro-entérite": ["diarrhée", "vomissements", "douleurs abdominales", "fièvre"],
"Rhume": ["nez bouché", "éternuements", "mal de gorge", "toux légère"],
"Pneumonie": ["toux avec flegme", "fièvre", "frissons", "difficulté à respirer"],
"Bronchite": ["toux persistante", "production de mucus", "fatigue", "essoufflement"],
"Anémie": ["fatigue extrême", "pâleur", "essoufflement", "maux de tête"],
"Hypertension": ["maux de tête", "essoufflement", "saignements de nez", "étourdissements"],
"Hypotension": ["étourdissements", "évanouissements", "vision floue", "nausées"],
"Allergie au pollen": ["éternuements", "nez qui coule", "yeux rouges", "démangeaisons"],
"Infection urinaire": ["brûlure en urinant", "envie pressante", "douleur au bas-ventre"],
"Varicelle": ["boutons rouges", "démangeaisons", "fièvre", "fatigue"],
"Rougeole": ["éruption cutanée", "fièvre", "toux", "nez qui coule", "yeux rouges"],
"Otite": ["douleur à l'oreille", "perte d'audition temporaire", "fièvre"],
"Sinusite": ["douleur faciale", "nez bouché", "maux de tête", "perte d'odorat"],
"Conjonctivite": ["yeux rouges", "démangeaisons", "écoulement oculaire"],
"Migraine": ["mal de tête intense", "nausées", "sensibilité à la lumière"],
"Appendicite": ["douleur vive à droite du ventre", "nausées", "fièvre"],
"Calculs rénaux": ["douleur intense au dos", "besoin d'uriner", "sang dans les urines"],
"Cholestérol": ["fatigue", "essoufflement", "douleurs thoraciques"],
"Dépression": ["tristesse persistante", "perte d'intérêt", "fatigue", "insomnie"],
"Anxiété": ["nervosité", "rythme cardiaque rapide", "tremblements", "transpiration"],
"Insomnie": ["difficulté à s'endormir", "réveil nocturne", "fatigue la journée"],
"Eczéma": ["plaques rouges", "démangeaisons", "peau sèche"],
"Psoriasis": ["plaques épaisses", "squames blanches", "démangeaisons"],
"Intolérance au lactose": ["ballonnements", "diarrhée", "gaz après produits laitiers"],
"Maladie de Crohn": ["douleurs abdominales chroniques", "diarrhée", "perte de poids"],
"Reflux gastrique": ["brûlures d'estomac", "remontées acides", "mal de gorge"],
"Ulcère d'estomac": ["douleur à l'estomac", "nausées", "ballonnements"],
"Hépatite": ["jaunisse", "fatigue", "douleurs abdominales", "nausées"],
"Hypothyroïdie": ["prise de poids", "fatigue", "frilosité", "constipation"],
"Hyperthyroïdie": ["perte de poids", "nervosité", "battements de cœur rapides"],
"Arthrose": ["douleurs articulaires", "raideur le matin", "perte de souplesse"],
"Rhumatisme": ["douleurs musculaires", "gonflement des articulations"],
"Lyme": ["tâche rouge circulaire", "fièvre", "maux de tête", "fatigue"],
"Paludisme": ["fièvre forte", "frissons", "transpiration", "maux de tête"],
"Dengue": ["forte fièvre", "douleurs derrière les yeux", "douleurs musculaires"],
"Zika": ["éruption cutanée", "fièvre", "douleurs articulaires", "yeux rouges"],
"Chikungunya": ["forte fièvre", "douleurs articulaires intenses", "fatigue"],
"Tuberculose": ["toux persistante avec sang", "perte de poids", "sueurs nocturnes"],
"Coqueluche": ["quintes de toux violentes", "difficulté à respirer"],
"Scarlatine": ["mal de gorge", "fièvre", "langue rouge", "éruption cutanée"],
"Mononucléose": ["grosse fatigue", "mal de gorge", "ganglions gonflés"],
"Herpès": ["petites bulles", "picotements", "démangeaisons"],
"Zona": ["douleur vive", "éruption cutanée d'un côté du corps"],
"Cystite": ["besoin fréquent d'uriner", "douleur au bassin"],
"Laryngite": ["extinction de voix", "mal de gorge", "toux sèche"]
}

# 3. PRÉPARATION DES SYMPTÔMES (Automatique)
options_symptomes = sorted(list(set([s for liste in maladies_data.values() for s in liste])))

# 4. INTERFACE UTILISATEUR
st.title("⚕️ Système d'Analyse Médicale")
st.write("Cet outil permet d'identifier des pathologies potentielles en fonction des symptômes renseignés.")

choix_utilisateur = st.multiselect("Veuillez sélectionner vos symptômes :", options_symptomes)

# 5. LOGIQUE DE CALCUL
      # --- NOUVELLE LOGIQUE D'ORDONNANCE ---
      resultats = []
      for maladie, symptomes in maladies_data.items():
         communs = [s for s in choix_utilisateur if s in symptomes]
         score = len(communs)
         if score > 0:
            resultats.append({"nom": maladie, "communs": communs, "score": score})

      resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)

      if resultats:
         st.info(f"### 📋 Résultats : {len(resultats)} pathologie(s) détectée(s)")
            # On affiche la meilleure en premier (l'ordonnance)
            top = resultats[0]
            st.success(f"**DIAGNOSTIC PRINCIPAL : {top['nom'].upper()}**")
            st.write(f"Symptômes correspondants : {', '.join(top['communs'])}")

         if len(resultats) > 1:
            with st.expander("Voir les autres diagnostics possibles"):
               for res in resultats[1:]:
                  st.write(f"🔸 **{res['nom']}** ({res['score']} symptômes communs)")
         trouve = True
