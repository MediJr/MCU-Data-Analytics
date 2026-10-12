import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. CHARGEMENT DES DONNÉES NETTOYÉES
# ============================================================

# On utilise le fichier nettoyé produit lors de l'étape précédente.
# Pourquoi ?
# L'EDA doit être réalisée sur la version validée des données,
# et non directement sur la source originale.

df = pd.read_csv("marvel_movies_dataset_clean.csv")


# ============================================================
# 2. PRÉPARATION DES VARIABLES
# ============================================================

# On reconvertit release_date en date.
# Pourquoi ?
# Même si cette variable a été nettoyée précédemment, la lecture
# d'un CSV transforme généralement les dates en chaînes de caractères.
# Cette conversion permet de pouvoir effectuer des analyses temporelles
# si nécessaire.

df["release_date"] = pd.to_datetime(df["release_date"])


# ============================================================
# 3. VUE GÉNÉRALE DU DATASET
# ============================================================

# On affiche le nombre de lignes et de colonnes.
# Pourquoi ?
# Cela permet de confirmer que l'EDA porte bien sur l'ensemble
# des 34 films et des 20 variables.

print("============================================================")
print("VUE GÉNÉRALE")
print("============================================================")

print("\nDimensions du dataset :", df.shape)


# On affiche les statistiques descriptives des variables numériques.
# Pourquoi ?
# Cela permet d'obtenir une première vision des distributions :
# moyenne, médiane, minimum, maximum et quartiles.

print("\nStatistiques descriptives :")
print(df.describe().round(2))


# ============================================================
# 4. INDICATEURS GÉNÉRAUX DU CATALOGUE
# ============================================================

# On calcule quelques indicateurs clés pour avoir une vision
# synthétique du catalogue.
# Pourquoi ?
# Ces indicateurs pourront être réutilisés plus tard dans
# le dashboard Power BI.

print("\n============================================================")
print("INDICATEURS CLÉS")
print("============================================================")

print(
    "\nBox-office mondial total :",
    round(df["worldwide_box_office_millions"].sum(), 2),
    "M$"
)

print(
    "Profit total :",
    round(df["profit_millions"].sum(), 2),
    "M$"
)

print(
    "Budget moyen :",
    round(df["production_budget_millions"].mean(), 2),
    "M$"
)

print(
    "Box-office mondial moyen :",
    round(df["worldwide_box_office_millions"].mean(), 2),
    "M$"
)

print(
    "Profit moyen :",
    round(df["profit_millions"].mean(), 2),
    "M$"
)

print(
    "ROI moyen :",
    round(df["roi_percentage"].mean(), 2),
    "%"
)

print(
    "Note IMDb moyenne :",
    round(df["imdb_rating"].mean(), 2),
    "/ 10"
)

print(
    "Rotten Tomatoes moyen :",
    round(df["rotten_tomatoes"].mean(), 2),
    "/ 100"
)

print(
    "Metacritic moyen :",
    round(df["metacritic_score"].mean(), 2),
    "/ 100"
)


# ============================================================
# 5. RÉPARTITION DU CATALOGUE PAR PHASE
# ============================================================

# On compte le nombre de films dans chaque phase.
# Pourquoi ?
# Le nombre de films doit être pris en compte lorsque l'on compare
# les performances moyennes des différentes phases.

films_par_phase = df["phase"].value_counts().sort_index()

print("\n============================================================")
print("RÉPARTITION DES FILMS PAR PHASE")
print("============================================================")

print(films_par_phase)


# ============================================================
# 6. PERFORMANCE COMMERCIALE : TOP 5
# ============================================================

# On sélectionne les films générant le plus de recettes mondiales.
# Pourquoi ?
# Cela permet d'identifier les films qui dominent commercialement
# le catalogue.

colonnes_financieres = [
    "movie_title",
    "production_budget_millions",
    "worldwide_box_office_millions",
    "profit_millions",
    "roi_percentage"
]

print("\n============================================================")
print("TOP 5 — BOX-OFFICE MONDIAL")
print("============================================================")

top_boxoffice = (
    df[colonnes_financieres]
    .sort_values(
        by="worldwide_box_office_millions",
        ascending=False
    )
    .head(5)
)

print(top_boxoffice.to_string(index=False))


# ============================================================
# 7. PERFORMANCE COMMERCIALE : TOP 5 PROFIT
# ============================================================

# On identifie les films générant le plus de profit absolu.
# Pourquoi ?
# Le box-office mesure les recettes alors que le profit tient
# également compte du budget de production.

print("\n============================================================")
print("TOP 5 — PROFIT")
print("============================================================")

top_profit = (
    df[colonnes_financieres]
    .sort_values(
        by="profit_millions",
        ascending=False
    )
    .head(5)
)

print(top_profit.to_string(index=False))


# ============================================================
# 8. RENTABILITÉ : TOP 5 ROI
# ============================================================

# On identifie les films ayant le meilleur retour sur investissement.
# Pourquoi ?
# Le ROI permet de comparer la rentabilité relative des films,
# indépendamment de leur niveau absolu de recettes.

print("\n============================================================")
print("TOP 5 — ROI")
print("============================================================")

top_roi = (
    df[colonnes_financieres]
    .sort_values(
        by="roi_percentage",
        ascending=False
    )
    .head(5)
)

print(top_roi.to_string(index=False))


# ============================================================
# 9. PERFORMANCE CRITIQUE
# ============================================================

# On calcule les principaux indicateurs statistiques des trois
# systèmes de notation.
# Pourquoi ?
# Objectif : comparer les performances critiques du catalogue.

notes = df[
    [
        "imdb_rating",
        "rotten_tomatoes",
        "metacritic_score"
    ]
]

print("\n============================================================")
print("PERFORMANCE CRITIQUE")
print("============================================================")

print("\nStatistiques des notes :")
print(notes.describe().round(2))


# Meilleur film selon IMDb.
print("\nFilm avec la meilleure note IMDb :")
print(
    df.loc[
        df["imdb_rating"].idxmax(),
        ["movie_title", "imdb_rating"]
    ].to_string()
)


# Meilleur film selon Rotten Tomatoes.
print("\nFilm avec le meilleur score Rotten Tomatoes :")
print(
    df.loc[
        df["rotten_tomatoes"].idxmax(),
        ["movie_title", "rotten_tomatoes"]
    ].to_string()
)


# Meilleur film selon Metacritic.
print("\nFilm avec le meilleur score Metacritic :")
print(
    df.loc[
        df["metacritic_score"].idxmax(),
        ["movie_title", "metacritic_score"]
    ].to_string()
)


# ============================================================
# 10. RELATION INVESTISSEMENT → RECETTES
# ============================================================

# On mesure la corrélation entre le budget de production
# et le box-office mondial.
# Pourquoi ?
# Objectif : savoir si les investissements sont associés
# aux recettes générées.

correlation_budget_boxoffice = (
    df[
        [
            "production_budget_millions",
            "worldwide_box_office_millions"
        ]
    ]
    .corr()
    .iloc[0, 1]
)

print("\n============================================================")
print("INVESTISSEMENT → RECETTES")
print("============================================================")

print(
    "\nCorrélation budget / box-office mondial :",
    round(correlation_budget_boxoffice, 2)
)


# ============================================================
# 11. RELATION NOTES → BOX-OFFICE
# ============================================================

# On mesure la corrélation entre les différents indicateurs
# critiques et le box-office.
# Pourquoi ?
# Cela permet d'identifier quels indicateurs critiques présentent
# la plus forte association avec la performance commerciale.

correlations_boxoffice = (
    df[
        [
            "imdb_rating",
            "rotten_tomatoes",
            "metacritic_score",
            "worldwide_box_office_millions"
        ]
    ]
    .corr()["worldwide_box_office_millions"]
)

print("\nCorrélations avec le box-office mondial :")
print(correlations_boxoffice.round(2))


# ============================================================
# 12. RELATION IMDb → ROI
# ============================================================

# On mesure la corrélation entre la note IMDb et le ROI.
# Pourquoi ?
# Cela permet de vérifier si les films ayant une meilleure
# appréciation du public présentent également une meilleure
# rentabilité relative.

correlation_imdb_roi = (
    df[
        [
            "imdb_rating",
            "roi_percentage"
        ]
    ]
    .corr()
    .iloc[0, 1]
)

print(
    "\nCorrélation IMDb / ROI :",
    round(correlation_imdb_roi, 2)
)


# ============================================================
# 13. PERFORMANCE FINANCIÈRE PAR PHASE
# ============================================================

# On calcule les performances moyennes de chaque phase.
# Pourquoi ?
# Objectif : comparer les performances des différentes
# phases du MCU.

performance_par_phase = (
    df.groupby("phase")[
        [
            "worldwide_box_office_millions",
            "profit_millions",
            "roi_percentage"
        ]
    ]
    .mean()
    .round(2)
)

print("\n============================================================")
print("PERFORMANCE FINANCIÈRE PAR PHASE")
print("============================================================")

print(performance_par_phase)


# ============================================================
# 14. PERFORMANCE CRITIQUE PAR PHASE
# ============================================================

# On calcule les notes critiques moyennes par phase.
# Pourquoi ?
# Cela permet de comparer non seulement la performance financière
# des phases, mais également leur réception critique.

notes_par_phase = (
    df.groupby("phase")[
        [
            "imdb_rating",
            "rotten_tomatoes",
            "metacritic_score"
        ]
    ]
    .mean()
    .round(2)
)

print("\n============================================================")
print("PERFORMANCE CRITIQUE PAR PHASE")
print("============================================================")

print(notes_par_phase)


# ============================================================
# 15. ÉVOLUTION DU BOX-OFFICE PAR ANNÉE
# ============================================================

# On calcule le box-office mondial moyen par année.
# Pourquoi ?
# Cela permet d'identifier les périodes de hausse ou de baisse
# des performances commerciales.

boxoffice_par_annee = (
    df.groupby("release_year")[
        "worldwide_box_office_millions"
    ]
    .mean()
    .round(2)
)

print("\n============================================================")
print("ÉVOLUTION DU BOX-OFFICE PAR ANNÉE")
print("============================================================")

print(boxoffice_par_annee)


# ============================================================
# 16. VISUALISATION — BUDGET / BOX-OFFICE
# ============================================================

# Chaque point représente un film.
# Pourquoi ?
# Le nuage de points permet de visualiser la relation entre
# l'investissement et les recettes.

plt.figure(figsize=(8, 5))

plt.scatter(
    df["production_budget_millions"],
    df["worldwide_box_office_millions"]
)

plt.title("Relation entre le budget et le box-office mondial")
plt.xlabel("Budget de production (millions de dollars)")
plt.ylabel("Box-office mondial (millions de dollars)")

plt.show()


# ============================================================
# 17. VISUALISATION — ROI MOYEN PAR PHASE
# ============================================================

# On compare visuellement le ROI moyen des différentes phases.
# Pourquoi ?
# Le graphique permet d'identifier rapidement
# les phases les plus et les moins rentables.

plt.figure(figsize=(8, 5))

plt.bar(
    performance_par_phase.index,
    performance_par_phase["roi_percentage"]
)

plt.title("ROI moyen par phase du MCU")
plt.xlabel("Phase")
plt.ylabel("ROI moyen (%)")

plt.show()


# ============================================================
# 18. VISUALISATION — BOX-OFFICE MOYEN PAR PHASE
# ============================================================

# On compare le box-office mondial moyen des différentes phases.
# Pourquoi ?
# Cela permet d'identifier les phases ayant généré les meilleures
# performances commerciales moyennes.

plt.figure(figsize=(8, 5))

plt.bar(
    performance_par_phase.index,
    performance_par_phase["worldwide_box_office_millions"]
)

plt.title("Box-office mondial moyen par phase du MCU")
plt.xlabel("Phase")
plt.ylabel("Box-office moyen (millions de dollars)")

plt.show()


# ============================================================
# 19. VISUALISATION — PERFORMANCE CRITIQUE
# ============================================================

# IMDb est initialement noté sur 10 alors que Rotten Tomatoes
# et Metacritic sont sur 100.
# On convertit donc uniquement IMDb sur une base 100 pour permettre
# une comparaison visuelle des niveaux moyens.
#
# Important :
# Cette conversion sert uniquement à faciliter la visualisation.
# Les trois plateformes utilisent des méthodologies différentes.

notes_moyennes = {
    "IMDb": df["imdb_rating"].mean() * 10,
    "Rotten Tomatoes": df["rotten_tomatoes"].mean(),
    "Metacritic": df["metacritic_score"].mean()
}

plt.figure(figsize=(8, 5))

plt.bar(
    notes_moyennes.keys(),
    notes_moyennes.values()
)

plt.title("Performance critique moyenne")
plt.xlabel("Indicateur critique")
plt.ylabel("Score moyen sur 100")

plt.show()


# ============================================================
# 20. VISUALISATION — ÉVOLUTION DU BOX-OFFICE
# ============================================================

# On représente l'évolution du box-office moyen par année.
# Pourquoi ?
# Une courbe permet de mieux visualiser les variations temporelles
# du catalogue.

plt.figure(figsize=(10, 5))

plt.plot(
    boxoffice_par_annee.index,
    boxoffice_par_annee.values,
    marker="o"
)

plt.title("Évolution du box-office mondial moyen")
plt.xlabel("Année de sortie")
plt.ylabel("Box-office moyen (millions de dollars)")

plt.show()


# ============================================================
# 21. VISUALISATION — PERFORMANCE CRITIQUE PAR PHASE
# ============================================================

# On compare les trois indicateurs critiques entre les phases.
# Pourquoi ?
# Cela permet de déterminer si les phases les plus performantes
# commercialement sont également celles qui obtiennent les
# meilleures évaluations critiques.

notes_phase_normalisees = notes_par_phase.copy()

# Conversion de la note IMDb sur une base 100 uniquement pour
# permettre la comparaison visuelle avec les deux autres scores.
notes_phase_normalisees["imdb_rating"] = (
    notes_phase_normalisees["imdb_rating"] * 10
)

plt.figure(figsize=(9, 5))

x = range(len(notes_phase_normalisees.index))
largeur = 0.25

plt.bar(
    [i - largeur for i in x],
    notes_phase_normalisees["imdb_rating"],
    width=largeur,
    label="IMDb"
)

plt.bar(
    x,
    notes_phase_normalisees["rotten_tomatoes"],
    width=largeur,
    label="Rotten Tomatoes"
)

plt.bar(
    [i + largeur for i in x],
    notes_phase_normalisees["metacritic_score"],
    width=largeur,
    label="Metacritic"
)

plt.xticks(
    list(x),
    notes_phase_normalisees.index
)

plt.title("Performance critique moyenne par phase")
plt.xlabel("Phase")
plt.ylabel("Score moyen sur 100")

plt.legend()

plt.show()


# ============================================================
# 22. VISUALISATION — IMDb / ROI
# ============================================================

# Chaque point représente un film.
# Pourquoi ?
# Cette visualisation permet d'observer directement la relation
# entre l'appréciation IMDb et la rentabilité du film.

plt.figure(figsize=(8, 5))

plt.scatter(
    df["imdb_rating"],
    df["roi_percentage"]
)

plt.title("Relation entre la note IMDb et le ROI")
plt.xlabel("Note IMDb")
plt.ylabel("ROI (%)")

plt.show()


# ============================================================
# 23. FIN DE L'EDA
# ============================================================

print("\n============================================================")
print("EDA TERMINÉE")
print("============================================================")

print(
    "\nLes principales dimensions retenues pour l'analyse ont été "
    "explorées : performance commerciale, performance critique, "
    "investissement, recettes, rentabilité, comparaison des phases "
    "et évolution temporelle."
)