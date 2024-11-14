import streamlit as st
import pandas as pd
import numpy as np
from styles import inject_css, inject_header  # Importer la fonction depuis styles.py
import random
import seaborn as sns
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta
import locale

# vecteur nombre de jour dans chaque mois de 2025
jours_par_mois_2025 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Vecteur depense, chiffre d'affaire et benefice pour chaque jour de l'année
depenses_vecteur = np.zeros(365)  
chiffre_affaire_vecteur = np.zeros(365)  
benefice_vecteur = np.zeros(365)  

#Encodage jour type pannes vecteur : 0 journee normal; 1 panne 1; 2 panne 2 ect
jour_type_pannes_vecteur = np.zeros(365)  

# Définir la date de début
start_date = datetime(2025, 1, 1)
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Définir la date de début
date_de_debut = datetime(2025, 1, 1)

# Créer une liste des jours de la semaine pour chaque jour de 2025
liste_jours_2025 = []
for i in range(365):
    date_actuelle = date_de_debut + timedelta(days=i)
    liste_jours_2025.append(date_actuelle.strftime('%A'))

# Données d'entrée utilisateur
st.sidebar.header("Caisse de départ")
caisse_depart = st.sidebar.number_input("Caisse de départ", value=1000)
# duree_blocage_investissement = st.sidebar.number_input('Durée minimale du blocage de l’investissement de chaque investisseur (mois)', value=6)

st.sidebar.header("Paramètres lié à l'achat d'un tractopells")
prix_unitaire_pelle = st.sidebar.number_input('Prix unitaire du tractopelle', value=80000)
nombre_pelle = st.sidebar.number_input('Nombre de tractopelle acheté', value = 1)
prix_douane_pelle = st.sidebar.number_input('Prix douane du tractopelle', value=2500)
prix_envoi_pelle = st.sidebar.number_input('Prix d’envoi du tractopelle', value=6500)

st.sidebar.header("Paramètres lié à l'achat d'un camion benne")
prix_unitaire_camion = st.sidebar.number_input('Prix unitaire du camion benne', value=30000)
nombre_camion = st.sidebar.number_input('Nombre de camion benne acheté', value=0)
prix_douane_camion = st.sidebar.number_input('Prix douane du camion benne', value=5000)
prix_envoi_camion = st.sidebar.number_input('Prix d’envoi du camion benne', value=5000)

# st.sidebar.header("Paramètres à l'achat des camion citerne")
# prix_unitaire_camion = st.sidebar.number_input('Prix unitaire du camion citerne', value=30000)
# nombre_camion = st.sidebar.number_input('Nombre de camion citerne acheté', value=0)
# prix_douane_camion = st.sidebar.number_input('Prix douane du camion citerne', value=5000)
# prix_envoi_camion = st.sidebar.number_input('Prix d’envoi du camion citerne', value=5000)

# st.sidebar.header("Paramètres à l'achat des camion citerne")
# prix_unitaire_camion = st.sidebar.number_input('Prix unitaire du camion citerne', value=30000)
# nombre_camion = st.sidebar.number_input('Nombre de camion citerne acheté', value=0)
# prix_douane_camion = st.sidebar.number_input('Prix douane du camion citerne', value=5000)
# prix_envoi_camion = st.sidebar.number_input('Prix d’envoi du camion citerne', value=5000)

st.sidebar.header("Paramètres associés aux salaires")
salaire_chauffeur_tractopelle = st.sidebar.number_input("Salaire mensuel d'un chauffeur de tractopelle", value=1000)
salaire_chauffeur_benne = st.sidebar.number_input("Salaire mensuel d'un chauffeur de camion benne", value=1000)
salaire_responsable = st.sidebar.number_input('Salaire mensuel du responsable', value = 1000)



# Beauté des ongles
inject_header()
inject_css()

st.header("Chiffre d'affaire et charges par machine")
# Créer deux colonnes
col1, col2 = st.columns(2)

# Placer rentabilite_jour_pelle dans la première colonne
with col1:
    rentabilite_jour_pelle = st.number_input("Chiffre d'affaire par jour d'un tractopelle (€)", value=1000, step=50)
    essence_mois_pelle  = st.number_input('Coût du carburant par mois par tractopelle', value=800)
    huile_mois_pelle  = st.number_input("Coût de l'huile et du lubifiant par mois par tractopelle", value=300)    
     
# Placer rentabilite_jour_camion dans la deuxième colonne
with col2:
    rentabilite_jour_camion = st.number_input("Chiffre d'affaire par jour d'un camion benne (€)", value = 550, step=50)
    essence_mois_camion = st.number_input('Coût du carburant par mois par camion benne', value=800)   

st.header("Emploi du temps")
# Créer deux colonnes
col1_jour, col2_jour = st.columns(2)
with col1_jour:
    st.subheader("Tractopelle")
    # Créer des cases à cocher pour chaque jour de la semaine (pré-cochées)
    lundi_tractopelle = st.checkbox('Lundi', value=True, key='lundi_tractopelle')
    mardi_tractopelle = st.checkbox('Mardi', value=True, key='mardi_tractopelle')
    mercredi_tractopelle = st.checkbox('Mercredi', value=True, key='mercredi_tractopelle')
    jeudi_tractopelle = st.checkbox('Jeudi', value=True, key='jeudi_tractopelle')
    vendredi_tractopelle = st.checkbox('Vendredi', value=False, key='vendredi_tractopelle')
    samedi_tractopelle = st.checkbox('Samedi', value=True, key='samedi_tractopelle')
    dimanche_tractopelle = st.checkbox('Dimanche', value=True, key='dimanche_tractopelle')

    # Liste des jours cochés pour le tractopelle
    jours_travail_tractopelle = []
    if lundi_tractopelle:
        jours_travail_tractopelle.append("lundi")
    if mardi_tractopelle:
        jours_travail_tractopelle.append("mardi")
    if mercredi_tractopelle:
        jours_travail_tractopelle.append("mercredi")
    if jeudi_tractopelle:
        jours_travail_tractopelle.append("jeudi")
    if vendredi_tractopelle:
        jours_travail_tractopelle.append("vendredi")
    if samedi_tractopelle:
        jours_travail_tractopelle.append("samedi")
    if dimanche_tractopelle:
        jours_travail_tractopelle.append("dimanche")
with col2_jour:
    st.subheader("Camion benne")
    # Créer des cases à cocher pour chaque jour de la semaine (pré-cochées)
    lundi_benne = st.checkbox('Lundi', value=True, key='lundi_benne')
    mardi_benne = st.checkbox('Mardi', value=True, key='mardi_benne')
    mercredi_benne = st.checkbox('Mercredi', value=True, key='mercredi_benne')
    jeudi_benne = st.checkbox('Jeudi', value=True, key='jeudi_benne')
    vendredi_benne = st.checkbox('Vendredi', value=True, key='vendredi_benne')
    samedi_benne = st.checkbox('Samedi', value=True, key='samedi_benne')
    dimanche_benne = st.checkbox('Dimanche', value=True, key='dimanche_benne')

    # Liste des jours cochés pour le camion benne
    jours_travail_camion = []
    if lundi_benne:
        jours_travail_camion.append("lundi")
    if mardi_benne:
        jours_travail_camion.append("mardi")
    if mercredi_benne:
        jours_travail_camion.append("mercredi")
    if jeudi_benne:
        jours_travail_camion.append("jeudi")
    if vendredi_benne:
        jours_travail_camion.append("vendredi")
    if samedi_benne:
        jours_travail_camion.append("samedi")
    if dimanche_benne:
        jours_travail_camion.append("dimanche")

# Calculs basés sur les formules fournies
capital_depart = (nombre_pelle * (prix_unitaire_pelle + prix_douane_pelle + prix_envoi_pelle) +
                  nombre_camion * (prix_unitaire_camion + prix_douane_camion + prix_envoi_camion)+ 
                  caisse_depart)

# Charges fixe et variable par jour
essence_jour_pelle = (nombre_pelle * essence_mois_pelle ) * 12 / 365
essence_jour_camion = ( nombre_camion * essence_mois_camion) * 12 / 365
huile_jour_pelle =nombre_pelle* huile_mois_pelle * 12 / 365
salaire_chauffeur_jour =(nombre_pelle * salaire_chauffeur_tractopelle + nombre_camion * salaire_chauffeur_benne) * 12 / 365
salaire_responsable_jour = salaire_responsable * 12 / 365

###################################################################        
charge_variable_par_jour = essence_jour_pelle + essence_jour_camion + huile_jour_pelle
charge_fixe_par_jour =  salaire_responsable_jour + salaire_chauffeur_jour
###############################################################################
depense_jour_normal = charge_variable_par_jour + charge_fixe_par_jour
##########################################################################
chiffre_affaire_tractopelle_jour = nombre_pelle*rentabilite_jour_pelle
chiffre_affaire_benne_jour = nombre_camion * rentabilite_jour_camion

chiffre_affaire_jour_normal =  chiffre_affaire_tractopelle_jour + chiffre_affaire_benne_jour




for indice, key in enumerate(liste_jours_2025):
    if key.lower() in jours_travail_tractopelle:
        depenses_vecteur[indice] =  essence_jour_pelle + huile_jour_pelle
        chiffre_affaire_vecteur[indice] =chiffre_affaire_tractopelle_jour
    if key.lower() in jours_travail_camion:
        depenses_vecteur[indice] = depenses_vecteur[indice] + essence_jour_camion
        chiffre_affaire_vecteur[indice] = chiffre_affaire_vecteur[indice] + chiffre_affaire_benne_jour

    if key.lower() in jours_travail_tractopelle or key.lower() in jours_travail_camion:
        depenses_vecteur[indice] = depenses_vecteur[indice] + salaire_responsable_jour

# Titre de la page
# Définir les paramètres du modèle
#st.header("Définition du modèle operationel prévisonnel")
# Créer un DataFrame initial pour que l'utilisateur puisse modifier les valeurs
data_type_panne_variables = {
    "Type de pannes": [
                 "Crevaison mineure", "Changement de pneu", 
                 "Problème hydraulique", "Accident de chantier"],
    "Jours d'arrêt par panne (jour)": [1, 10, 5, 1],  # Valeurs par défaut
    "Nombre de pannes sur l'année (jour)": [0, 0, 0, 0],  # Valeurs par défaut
}

# Créer un DataFrame
# df_data_type_panne = pd.DataFrame(data_type_panne_variables)

# Utilisation de st.data_editor pour permettre à l'utilisateur de modifier les valeurs
#editable_df_data_type_panne = st.data_editor(df_data_type_panne)

# Créer un DataFrame avec 1 ligne et 2 colonnes
#data_total = {
#    "Nombre de jours de pannes sur l'année": [editable_df_data_type_panne['Nombre de pannes sur l\'année (jour)'].sum()]  # Valeur de la deuxième colonne
#}

# Ajouter une ligne "Total"
#df_total = pd.DataFrame(data_total, index=["Total"])
# Afficher le tableau avec st.table()
#st.dataframe(df_total)
# Récupérer les nouvelles valeurs depuis le tableau

# jour_arret_crevaison_mineur = editable_df_data_type_panne.loc[0, "Jours d'arrêt par panne (jour)"]
#jour_arret_changement_pneu = editable_df_data_type_panne.loc[1, "Jours d'arrêt par panne (jour)"]
#jour_arret_probleme_hydrolique = editable_df_data_type_panne.loc[2, "Jours d'arrêt par panne (jour)"]
#jour_arret_accident_chantier = editable_df_data_type_panne.loc[3, "Jours d'arrêt par panne (jour)"]

#jour_arret_crevaison_mineur_frequentiel = editable_df_data_type_panne.loc[0, "Nombre de pannes sur l'année (jour)"]
#jour_arret_changement_pneu_frequentiel = editable_df_data_type_panne.loc[1, "Nombre de pannes sur l'année (jour)"]
#jour_arret_probleme_hydrolique_frequentiel = editable_df_data_type_panne.loc[2, "Nombre de pannes sur l'année (jour)"]
#jour_arret_accident_chantier_frequentiel = editable_df_data_type_panne.loc[3, "Nombre de pannes sur l'année (jour)"]

cout_carburant_jour = essence_jour_pelle + essence_jour_camion
cout_main_oeuvre_jour = salaire_responsable_jour + salaire_chauffeur_jour
cout_huile_jour = huile_jour_pelle


# Exemple d'emploi du temps (modifiable selon vos besoins)
st.header("Description financière et opérationelle journalières")
ressources_tab, cout_revenu_journalier_tab = \
st.tabs(["Gestion des ressources journalières", "Coûts et revenus journaliers"])

#with planification_tab:
#    data_planification = {
#        "Heure": ["07h00-07h30", "07h30-08h00", "08h00-09h00", "09h00-12h00", "12h00-13h00", "13h00-16h00", "16h00-16h30", "16h30-17h00", "17h00-17h30"],
#        "Tâche": [
#            "Briefing", "Vérification des machines", "Départ vers le chantier", "Travail sur le chantier (matin)",
#            "Pause déjeuner", "Travail sur le chantier (après-midi)", "Retour à l'entrepôt", 
#            "Inspection et entretien des machines", "Briefing de fin de journée"
#        ],
#        "Détails/Actions": [
#            "Réunion pour assigner les tâches du jour", "Contrôle du matériel, carburant, huile, état des pneus", 
#            "Transport de l'équipement au chantier", "Terrassement, excavation, travaux de préparation",
#            "Pause pour les employés", "Continuation des travaux sur le chantier", 
#            "Retour des machines à l'entrepôt ou stationnement sur place", 
#            "Vérification des machines : huile, carburant, maintenance", 
#            "Discussion sur l'avancement des travaux, préparation du lendemain"
#        ],
#        "Personne/Responsable": [
#            "Chef d'équipe", "Mécanicien", "Chauffeur", "Chauffeur et ouvriers", "Tous les employés", 
#            "Chauffeur et ouvriers", "Chauffeur", "Mécanicien", "Chef d'équipe"
#        ]
#    }
#    df = pd.DataFrame(data_planification)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
#    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

#    st.dataframe(df)

with ressources_tab:
    data_ressources = {
    "Type de dépense": ["Carburant", "Huile et lubrifiant"],
    "Coût journalier (€)": [cout_carburant_jour, cout_huile_jour],
    "Commentaire": [
        "Varie en fonction de la durée et de l'intensité du travail", 
        "Changement ou ajout régulier"
    ]
}

    df = pd.DataFrame(data_ressources)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    st.dataframe(df)

with cout_revenu_journalier_tab:
    depense_euro_jour = depense_jour_normal
    chiffre_affaire_jour_euro = chiffre_affaire_jour_normal
    benefice_jour_euro = chiffre_affaire_jour_euro - depense_euro_jour
    data_cout_revenu_journalier = {
        "Variable financière et comptable journalière": [ "Chiffre d'affaire","Dépense", "Bénéfice"],
        "Valeur (€)": [chiffre_affaire_jour_euro,depense_euro_jour,  benefice_jour_euro ]
    }
    df = pd.DataFrame(data_cout_revenu_journalier)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    st.dataframe(df)

#with accident_tab:
#    data_accident = {
#        "Type d'accident": [
#            "Crevaison mineure", 
#            "Crevaison nécessitant un changement de pneu", 
#            "Défaillance du système hydraulique", 
#            "Accident sur le chantier"
#        ],
#        "Arrêt des opérations du à la panne (jour)": [
#             str(jour_arret_crevaison_mineur), 
#             str(jour_arret_changement_pneu), 
#             str(jour_arret_probleme_hydrolique), 
#             str(jour_arret_accident_chantier) 
#        ],
#        "Coût estimé (€)": [
#            "100 ", 
#            "5000 ", 
#            "500 ", 
#            "200 "
#        ],
#        "Commentaire": [
#            "Petite réparation rapide sur place", 
#            "Nécessite un changement de pneu", 
#            "Réparation coûteuse nécessitant un expert", 
#            "Assurance prend en charge une partie"
#        ]
#    }
    
    # Créer le DataFrame
#    df_accident = pd.DataFrame(data_accident)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
#    df_accident[df_accident.select_dtypes(include=[np.number]).columns] = df_accident.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    # Afficher le tableau avec Streamlit
#    st.dataframe(df_accident)

# Creation des vecteurs dépenses, chiffre d'affaire et benefice pour chaque jours de l'année    

benefice_vecteur = chiffre_affaire_vecteur - depenses_vecteur

data_benefice_total = {
    "Capital de départ (€)" : capital_depart,
"Bénéfice annuel (€)" : np.sum(benefice_vecteur)
    
}
# Créer le DataFrame
df = pd.DataFrame(data_benefice_total, index=[0])

# Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')
# Afficher le tableau avec Streamlit
st.dataframe(df)

# Données pour le graphique
temps = ['Départ', 'Achats', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
caisse_entreprise_vecteur = [round(capital_depart, 2), round(caisse_depart, 2)]  # Instants initiaux


start = 0
duree_rentabilisation = 0
# Calcul de l'évolution de la caisse
nouvelle_valeur = round(caisse_depart, 2)
for i in range(1, 13):  # Ajout des données pour chaque mois
    if round(caisse_depart, 2) >= 0:
         benefice_par_mois = np.sum(benefice_vecteur[start:start + jours_par_mois_2025[i-1]])  # Somme des bénéfices pour le mois
         start += jours_par_mois_2025[i-1]  # Mettre à jour le début du prochain mois
        
         nouvelle_valeur = nouvelle_valeur + benefice_par_mois
         caisse_entreprise_vecteur.append(nouvelle_valeur)
    else:
        caisse_entreprise_vecteur.append(round(caisse_depart, 2))

duree_rentabilisation = math.ceil( capital_depart / (np.sum(benefice_vecteur) / 12 ) )

# Création du graphique en barres avec Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=temps, y=caisse_entreprise_vecteur, color='skyblue', ax=ax)

# Définir le titre et les labels
ax.set_title(f"Capital de départ = $\mathbf{{{ capital_depart }}}$ €\nBénéfice mensuel = $\mathbf{{{int(np.sum(benefice_vecteur) / 12 )}}}$ €\nDurée de rentabilité: $\mathbf{{{int(duree_rentabilisation)}}}$ mois", fontsize=14)
ax.set_xlabel("Temps", fontsize=12)
ax.set_ylabel("Montant en caisse (€)", fontsize=12)

# Ajuster la taille et la rotation des étiquettes de l'axe des abscisses
ax.tick_params(axis='x', labelsize=8)  # Taille de police des labels de l'axe des abscisses
plt.xticks(rotation=45)

# Afficher le graphique dans Streamlit ou dans un notebook
st.pyplot(fig)  # Si vous êtes dans Streamlit