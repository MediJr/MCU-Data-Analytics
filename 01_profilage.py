import pandas as pd


# ============================================================
# 1. CHARGEMENT DES DONNÉES
# ============================================================

# On charge le fichier CSV dans un DataFrame Pandas.
# Objectif : disposer des données dans une structure permettant
# de réaliser notre inspection et notre analyse.
df = pd.read_csv("marvel_movies_dataset.csv")


# ============================================================
# 2. VÉRIFICATION DES DIMENSIONS
# ============================================================

# On vérifie le nombre de lignes et de colonnes.
# Pourquoi ?
# Cela permet de connaître la taille du dataset et de vérifier
# qu'il correspond à ce qui est annoncé dans la documentation.
print("Dimensions du dataset :", df.shape)


# ============================================================
# 3. VÉRIFICATION DES COLONNES
# ============================================================

# On affiche les noms des colonnes.
# Pourquoi ?
# Cela permet de vérifier la structure du dataset et de s'assurer
# que les variables attendues sont bien présentes.
print("\nColonnes :")
print(df.columns)


# ============================================================
# 4. VÉRIFICATION DES TYPES DE DONNÉES
# ============================================================

# On affiche le type détecté par Pandas pour chaque colonne.
# Pourquoi ?
# Une colonne peut contenir des données valides mais avoir un
# mauvais type.
#
# Exemple :
# release_date représente une date, mais Pandas l'a détectée
# comme une chaîne de caractères (str).
#
# IMPORTANT :
# On constate le problème pendant le profilage.
# La correction sera effectuée plus tard pendant le nettoyage.
print("\nTypes de données :")
print(df.dtypes)


# ============================================================
# 5. VÉRIFICATION DES VALEURS MANQUANTES
# ============================================================

# On compte le nombre de valeurs manquantes dans chaque colonne.
# Pourquoi ?
# Les valeurs manquantes peuvent empêcher certaines analyses
# et peuvent nécessiter un traitement pendant le nettoyage.
print("\nValeurs manquantes :")
print(df.isnull().sum())


# ============================================================
# 6. VÉRIFICATION DES DOUBLONS
# ============================================================

# On recherche les lignes complètement identiques.
# Pourquoi ?
# Des lignes dupliquées peuvent fausser les statistiques,
# les calculs et les analyses.
#
# Ici, nous voulons seulement identifier le problème.
# Nous ne supprimons encore aucune donnée.
print("\nDoublons :", df.duplicated().sum())


# ============================================================
# 7. VÉRIFICATION DE L'UNICITÉ DE L'IDENTIFIANT
# ============================================================

# On compte le nombre de movie_id différents.
# Pourquoi ?
# movie_id sert à identifier chaque film.
# Nous devons donc vérifier qu'un même identifiant ne correspond
# pas à plusieurs films.
#
# Notre dataset contient 34 lignes.
# Nous nous attendons donc idéalement à avoir 34 IDs uniques.
print("\nIDs uniques :", df["movie_id"].nunique())


# ============================================================
# 8. OBSERVATION DES PREMIÈRES LIGNES
# ============================================================

# On affiche les 5 premières lignes du dataset.
# Pourquoi ?
# Les statistiques ne suffisent pas toujours.
# L'observation directe permet de repérer des anomalies visibles :
# formats inattendus, valeurs étranges, colonnes mal interprétées,
# etc.
#
# Cette étape permet également de mieux comprendre concrètement
# la structure des données avant de commencer le nettoyage.
print("\nPremières lignes du dataset :")
print(df.head())


# ============================================================
# 9. EXAMEN DES VALEURS CATÉGORIELLES
# ============================================================

# On affiche les différentes valeurs présentes dans la colonne phase.
# Pourquoi ?
# "phase" est une variable catégorielle.
# Nous voulons vérifier quelles catégories existent réellement
# dans notre dataset et combien de films appartiennent à chacune.
print("\nRépartition des films par phase :")
print(df["phase"].value_counts())


# ============================================================
# 10. VÉRIFICATION DE LA COHÉRENCE PHASE / PHASE_NUMBER
# ============================================================

# On compare la valeur textuelle de "phase" avec la valeur numérique
# de "phase_number".
# Pourquoi ?
# Ces deux colonnes représentent la même information sous deux formes.
# Elles doivent donc rester cohérentes entre elles.
#
# On extrait le numéro contenu dans "phase" puis on le compare
# à "phase_number".
phase_number_from_text = df["phase"].str.extract(r"(\d+)")[0].astype(int)

print("\nIncohérences entre phase et phase_number :")
print((phase_number_from_text != df["phase_number"]).sum())


# ============================================================
# 11. CONTRÔLE DES ANNÉES DE SORTIE
# ============================================================

# On calcule l'année minimale et l'année maximale présentes
# dans le dataset.
# Pourquoi ?
# Le type "int64" nous indique seulement que ce sont des nombres.
# Il ne nous dit pas si les valeurs sont plausibles.
#
# Ce contrôle permet de repérer une année manifestement aberrante
# qui pourrait révéler une erreur de saisie ou de collecte.
print("\nAnnée de sortie minimale :", df["release_year"].min())
print("Année de sortie maximale :", df["release_year"].max())


# ============================================================
# 12. VÉRIFICATION DE LA COHÉRENCE DATE / ANNÉE
# ============================================================

# On convertit temporairement "release_date" en date afin
# d'extraire son année.
# Pourquoi ?
# "release_date" et "release_year" contiennent une information
# liée : l'année présente dans la date doit correspondre à
# la valeur de "release_year".
#
# Cette conversion est uniquement utilisée pour le contrôle.
# Le nettoyage définitif de "release_date" sera effectué plus tard.

release_date_temp = pd.to_datetime(df["release_date"], errors="coerce")

# On extrait l'année de la date.
annee_extraite = release_date_temp.dt.year

# On compare l'année extraite avec "release_year".
incoherences_date_annee = (
    annee_extraite != df["release_year"]
).sum()

print("\nIncohérences entre release_date et release_year :",
      incoherences_date_annee)


# ============================================================
# 13. STATISTIQUES DESCRIPTIVES DES VARIABLES NUMÉRIQUES
# ============================================================

# On calcule les principales statistiques des colonnes numériques.
# Pourquoi ?
# Le type d'une colonne ne garantit pas que ses valeurs sont
# correctes.
#
# Ces statistiques permettent notamment d'observer :
# - le nombre de valeurs ;
# - la moyenne ;
# - la dispersion ;
# - les valeurs minimales et maximales ;
# - les quartiles.
#
# Elles permettent donc de repérer d'éventuelles valeurs
# inhabituelles avant l'analyse.
print("\nStatistiques descriptives :")
print(df.describe())


# ============================================================
# 14. CONTRÔLE DES BORNES MÉTIER
# ============================================================

# On vérifie quelques limites évidentes définies par la nature
# des variables.
#
# Pourquoi ?
# Certaines variables possèdent des limites logiques.
#
# Par exemple :
# - IMDb est normalement noté sur 10 ;
# - Rotten Tomatoes est exprimé sur 100 ;
# - Metacritic est exprimé sur 100 ;
# - un temps d'exécution ne peut pas être négatif.
#
# Nous cherchons uniquement à détecter les valeurs qui sortent
# de ces limites. Nous ne les corrigeons pas ici.

print("\nValeurs IMDb hors de [0, 10] :")
print(((df["imdb_rating"] < 0) | (df["imdb_rating"] > 10)).sum())

print("\nValeurs Rotten Tomatoes hors de [0, 100] :")
print(((df["rotten_tomatoes"] < 0) | (df["rotten_tomatoes"] > 100)).sum())

print("\nValeurs Metacritic hors de [0, 100] :")
print(((df["metacritic_score"] < 0) | (df["metacritic_score"] > 100)).sum())

print("\nDurées négatives :")
print((df["runtime_minutes"] < 0).sum())
# ============================================================
# DATA QUALITY — 1. VALIDITÉ / CONFORMITÉ
# ============================================================

# On vérifie si toutes les valeurs de release_date peuvent
# être interprétées comme de vraies dates.
#
# Pourquoi ?
# Une colonne peut être stockée comme du texte tout en contenant
# des dates valides. Avant de la convertir définitivement,
# nous devons vérifier que son contenu respecte bien le format
# attendu.
#
# errors="coerce" transforme une valeur impossible à interpréter
# en NaT (Not a Time), ce qui nous permet ensuite de les compter.

release_date_check = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

dates_invalides = release_date_check.isna().sum()

print("\nDates invalides :", dates_invalides)
# ============================================================
# DATA QUALITY — 2. COHÉRENCE FINANCIÈRE
# ============================================================

# On vérifie que le profit enregistré correspond bien
# à la différence entre le box-office mondial et le budget.
#
# Pourquoi ?
# Ces trois variables sont liées mathématiquement.
# Si elles ne respectent pas cette relation, cela indique
# une incohérence dans les données.

profit_calcule = (
    df["worldwide_box_office_millions"]
    - df["production_budget_millions"]
)

incoherences_profit = (
    profit_calcule != df["profit_millions"]
).sum()

print("\nIncohérences dans le calcul du profit :", incoherences_profit)
# ============================================================
# DATA QUALITY — 3. COHÉRENCE DU POURCENTAGE DOMESTIQUE
# ============================================================

# On recalcule le pourcentage domestique à partir des données
# financières disponibles.
#
# Pourquoi ?
# domestic_percentage dépend directement du box-office domestique
# et du box-office mondial.
# Nous vérifions donc que la valeur enregistrée respecte cette
# relation mathématique.

domestic_percentage_calcule = (
    df["domestic_box_office_millions"]
    / df["worldwide_box_office_millions"]
) * 100

# On utilise une tolérance très faible car les pourcentages
# peuvent avoir été arrondis dans le dataset.
incoherences_domestic_percentage = (
    (domestic_percentage_calcule - df["domestic_percentage"]).abs() > 0.01
).sum()

print(
    "\nIncohérences dans domestic_percentage :",
    incoherences_domestic_percentage
)
# ============================================================
# DATA QUALITY — 4. COHÉRENCE DU ROI
# ============================================================

# On recalcule le ROI à partir du profit et du budget.
#
# Pourquoi ?
# Le ROI représente le gain réalisé par rapport au coût
# de l'investissement.
#
# Pour notre dataset :
# ROI = profit / budget × 100
#
# Nous vérifions donc que la valeur enregistrée dans
# roi_percentage respecte cette relation.

roi_calcule = (
    df["profit_millions"]
    / df["production_budget_millions"]
) * 100

# Une petite tolérance est utilisée afin de tenir compte
# d'éventuels arrondis dans les valeurs du dataset.
incoherences_roi = (
    (roi_calcule - df["roi_percentage"]).abs() > 0.01
).sum()

print("\nIncohérences dans roi_percentage :", incoherences_roi)