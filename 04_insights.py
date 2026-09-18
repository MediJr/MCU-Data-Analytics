import pandas as pd


# ============================================================
# 1. CHARGEMENT DES DONNÉES
# ============================================================

# On utilise le dataset nettoyé.
# Pourquoi ?
# Les insights doivent être calculés à partir des données
# validées lors des étapes précédentes.

df = pd.read_csv("marvel_movies_dataset_clean.csv")


# ============================================================
# 2. INDICATEURS COMMERCIAUX GLOBAUX
# ============================================================

# On calcule les principaux indicateurs commerciaux du catalogue.
# Pourquoi ?
# Le client souhaite comprendre la performance commerciale
# globale des films du MCU.

boxoffice_total = df["worldwide_box_office_millions"].sum()
profit_total = df["profit_millions"].sum()

boxoffice_moyen = df["worldwide_box_office_millions"].mean()
profit_moyen = df["profit_millions"].mean()

budget_total = df["production_budget_millions"].sum()
budget_moyen = df["production_budget_millions"].mean()


print("============================================================")
print("1. PERFORMANCE COMMERCIALE GLOBALE")
print("============================================================")

print(
    "\nBudget total investi :",
    round(budget_total, 2),
    "M$"
)

print(
    "Budget moyen par film :",
    round(budget_moyen, 2),
    "M$"
)

print(
    "Box-office mondial total :",
    round(boxoffice_total, 2),
    "M$"
)

print(
    "Box-office mondial moyen :",
    round(boxoffice_moyen, 2),
    "M$"
)

print(
    "Profit total :",
    round(profit_total, 2),
    "M$"
)

print(
    "Profit moyen :",
    round(profit_moyen, 2),
    "M$"
)


# ============================================================
# 3. FILMS LES PLUS PERFORMANTS COMMERCIALEMENT
# ============================================================

# On identifie les films ayant généré les plus gros box-offices.
# Pourquoi ?
# Cela permet de déterminer quels films contribuent le plus
# à la performance commerciale du catalogue.

top_commercial = (
    df[
        [
            "movie_title",
            "worldwide_box_office_millions",
            "profit_millions"
        ]
    ]
    .sort_values(
        by="worldwide_box_office_millions",
        ascending=False
    )
    .head(5)
)

print("\n============================================================")
print("2. TOP 5 — PERFORMANCE COMMERCIALE")
print("============================================================")

print(top_commercial.to_string(index=False))


# ============================================================
# 4. ANALYSE DE LA RENTABILITÉ
# ============================================================

# On calcule le ROI moyen du catalogue.
# Pourquoi ?
# Le ROI mesure la rentabilité relative des investissements.

roi_moyen = df["roi_percentage"].mean()

print("\n============================================================")
print("3. RENTABILITÉ DU CATALOGUE")
print("============================================================")

print(
    "\nROI moyen du catalogue :",
    round(roi_moyen, 2),
    "%"
)


# On identifie les films ayant le meilleur ROI.
# Pourquoi ?
# Un film peut générer moins de recettes qu'un blockbuster
# mais être plus rentable proportionnellement à son budget.

top_rentabilite = (
    df[
        [
            "movie_title",
            "production_budget_millions",
            "profit_millions",
            "roi_percentage"
        ]
    ]
    .sort_values(
        by="roi_percentage",
        ascending=False
    )
    .head(5)
)

print("\nTop 5 — Films les plus rentables :")
print(top_rentabilite.to_string(index=False))


# ============================================================
# 5. COMPARAISON DES PHASES DU MCU
# ============================================================

# On regroupe les films par phase.
# Pourquoi ?
# Le client souhaite comparer les performances des différentes
# phases du MCU.

performance_phases = (
    df.groupby("phase")
    .agg(
        nombre_films=("movie_id", "count"),
        budget_moyen=("production_budget_millions", "mean"),
        boxoffice_moyen=("worldwide_box_office_millions", "mean"),
        profit_moyen=("profit_millions", "mean"),
        roi_moyen=("roi_percentage", "mean")
    )
    .round(2)
)

print("\n============================================================")
print("4. PERFORMANCE FINANCIÈRE PAR PHASE")
print("============================================================")

print(performance_phases)


# ============================================================
# 6. PERFORMANCE CRITIQUE GLOBALE
# ============================================================

# On calcule les moyennes des trois indicateurs critiques.
# Pourquoi ?
# Le client souhaite comparer la réception critique du catalogue.

imdb_moyen = df["imdb_rating"].mean()
rotten_tomatoes_moyen = df["rotten_tomatoes"].mean()
metacritic_moyen = df["metacritic_score"].mean()

print("\n============================================================")
print("5. PERFORMANCE CRITIQUE")
print("============================================================")

print(
    "\nIMDb moyen :",
    round(imdb_moyen, 2),
    "/ 10"
)

print(
    "Rotten Tomatoes moyen :",
    round(rotten_tomatoes_moyen, 2),
    "/ 100"
)

print(
    "Metacritic moyen :",
    round(metacritic_moyen, 2),
    "/ 100"
)


# ============================================================
# 7. MEILLEURES PERFORMANCES CRITIQUES
# ============================================================

# On identifie le meilleur film selon chaque indicateur critique.
# Pourquoi ?
# Cela permet de déterminer quels films se distinguent
# auprès du public et des critiques.

meilleur_imdb = df.loc[
    df["imdb_rating"].idxmax(),
    ["movie_title", "imdb_rating"]
]

meilleur_rotten = df.loc[
    df["rotten_tomatoes"].idxmax(),
    ["movie_title", "rotten_tomatoes"]
]

meilleur_metacritic = df.loc[
    df["metacritic_score"].idxmax(),
    ["movie_title", "metacritic_score"]
]

print("\nMeilleure note IMDb :")
print(meilleur_imdb.to_string())

print("\nMeilleur score Rotten Tomatoes :")
print(meilleur_rotten.to_string())

print("\nMeilleur score Metacritic :")
print(meilleur_metacritic.to_string())


# ============================================================
# 8. PERFORMANCE CRITIQUE PAR PHASE
# ============================================================

# On calcule les notes critiques moyennes par phase.
# Pourquoi ?
# Cela permet de comparer la réception critique des différentes
# phases du MCU et de la mettre en parallèle avec leur performance
# financière.

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
print("6. PERFORMANCE CRITIQUE PAR PHASE")
print("============================================================")

print(notes_par_phase)


# ============================================================
# 9. RELATION INVESTISSEMENT → RECETTES
# ============================================================

# On mesure la corrélation entre le budget et le box-office.
# Pourquoi ?
# Le client souhaite étudier la relation entre les investissements
# réalisés et les recettes générées.

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
print("7. INVESTISSEMENT → RECETTES")
print("============================================================")

print(
    "\nCorrélation budget / box-office :",
    round(correlation_budget_boxoffice, 2)
)


# ============================================================
# 10. RELATION PERFORMANCE CRITIQUE → RECETTES
# ============================================================

# On mesure les corrélations entre les notes critiques
# et le box-office mondial.
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
    .drop("worldwide_box_office_millions")
)

print("\n============================================================")
print("8. PERFORMANCE CRITIQUE → RECETTES")
print("============================================================")

print(
    correlations_boxoffice.round(2)
)


# ============================================================
# 11. RELATION PERFORMANCE CRITIQUE → RENTABILITÉ
# ============================================================

# On mesure la corrélation entre IMDb et le ROI.
# Pourquoi ?
# Cela permet d'étudier si une meilleure appréciation sur IMDb
# est associée à une meilleure rentabilité.

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

print("\n============================================================")
print("9. PERFORMANCE CRITIQUE → RENTABILITÉ")
print("============================================================")

print(
    "\nCorrélation IMDb / ROI :",
    round(correlation_imdb_roi, 2)
)


# ============================================================
# 12. ÉVOLUTION TEMPORELLE
# ============================================================

# On calcule le box-office moyen par année.
# Pourquoi ?
# Le client souhaite comprendre les tendances de performance
# du catalogue dans le temps.

boxoffice_par_annee = (
    df.groupby("release_year")[
        "worldwide_box_office_millions"
    ]
    .mean()
    .round(2)
)

print("\n============================================================")
print("10. ÉVOLUTION DU BOX-OFFICE")
print("============================================================")

print(boxoffice_par_annee)


# ============================================================
# 13. MEILLEURE ET PLUS FAIBLE PERFORMANCE PAR BOX-OFFICE
# ============================================================

# On identifie les extrêmes du catalogue.
# Pourquoi ?
# Cela permet de compléter l'analyse avec les cas les plus
# performants et les moins performants commercialement.

film_max_boxoffice = df.loc[
    df["worldwide_box_office_millions"].idxmax(),
    [
        "movie_title",
        "worldwide_box_office_millions",
        "profit_millions",
        "roi_percentage"
    ]
]

film_min_boxoffice = df.loc[
    df["worldwide_box_office_millions"].idxmin(),
    [
        "movie_title",
        "worldwide_box_office_millions",
        "profit_millions",
        "roi_percentage"
    ]
]

print("\n============================================================")
print("11. EXTRÊMES COMMERCIAUX")
print("============================================================")

print("\nMeilleur box-office :")
print(film_max_boxoffice.to_string())

print("\nPlus faible box-office :")
print(film_min_boxoffice.to_string())


# ============================================================
# 14. RÉSUMÉ DES PRINCIPAUX INDICATEURS
# ============================================================

# On rassemble les indicateurs essentiels dans un dictionnaire.
# Pourquoi ?
# Cette synthèse pourra servir de base pour construire les KPI
# du futur dashboard Power BI.

kpis = {
    "Films analysés": len(df),
    "Box-office total (M$)": round(boxoffice_total, 2),
    "Profit total (M$)": round(profit_total, 2),
    "Box-office moyen (M$)": round(boxoffice_moyen, 2),
    "Profit moyen (M$)": round(profit_moyen, 2),
    "ROI moyen (%)": round(roi_moyen, 2),
    "IMDb moyen": round(imdb_moyen, 2),
    "Rotten Tomatoes moyen": round(rotten_tomatoes_moyen, 2),
    "Metacritic moyen": round(metacritic_moyen, 2),
    "Corrélation budget / box-office": round(
        correlation_budget_boxoffice,
        2
    ),
    "Corrélation IMDb / box-office": round(
        correlations_boxoffice["imdb_rating"],
        2
    ),
    "Corrélation IMDb / ROI": round(
        correlation_imdb_roi,
        2
    )
}

print("\n============================================================")
print("12. SYNTHÈSE DES KPI")
print("============================================================")

for indicateur, valeur in kpis.items():
    print(f"{indicateur} : {valeur}")


# ============================================================
# FIN DE L'ANALYSE DES INSIGHTS
# ============================================================

print("\n============================================================")
print("ANALYSE DES INSIGHTS TERMINÉE")
print("============================================================")