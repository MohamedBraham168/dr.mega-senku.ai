# --- LOGIQUE FINALE ---
st.write("### 📝 Sélectionnez vos symptômes :")

# Cette ligne magique crée la liste de TOUS les symptômes de ton dictionnaire sans doublons
options_symptomes = sorted(list(set([s for liste in maladies_data.values() for s in liste])))

# Une barre de sélection multiple (très pro et facile à utiliser)
choix_utilisateur = st.multiselect("Recherchez ou sélectionnez vos symptômes :", options_symptomes)

if st.button("🩺 Lancer le diagnostic médical"):
   if choix_utilisateur:
      st.write("---")
      st.subheader("Analyse du Dr. IA :")
      trouve = False

      for maladie, symptomes in maladies_data.items():
         # On compte combien de symptômes correspondent
         nb_correspondances = len(set(choix_utilisateur) & set(symptomes))
         
         if nb_correspondances > 0:
            st.success(f"Possibilité : **{maladie.upper()}**")
            st.info(f"Symptômes signatures : {', '.join(symptomes)}")
            trouve = True
      
      if not trouve:
      st.warning("Aucune correspondance exacte trouvée. Essayez d'ajouter d'autres symptômes.")

st.write("---")
st.caption("⚠️ Rappel : Cette IA ne remplace pas un vrai médecin.")
   else:
   st.error("Veuillez sélectionner au moins un symptôme pour l'analyse.")
