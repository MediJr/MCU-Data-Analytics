import pandas as pd


# ============================================================
# 1. CHARGEMENT DE LA SOURCE ORIGINALE
# ============================================================

# On recharge le fichier CSV original.
# Pourquoi ?
# Le nettoyage doit partir de la source originale afin de
# conserver une séparation claire entre les données brutes
# et les données transformées.
#
# IMPORTANT :
# On ne modifie jamais directement le fichier CSV original.

df = pd.read_csv("marvel_movies_dataset.csv")
print("Dimensions de la source :", df.shape)

# ============================================================
# 2. CONVERSION DE RELEASE_DATE
# ============================================================

# On convertit release_date de texte (str) vers un véritable
# type date (datetime).
#
# Pourquoi ?
# Le profilage a montré que release_date est actuellement
# stockée comme du texte alors qu'elle représente une date.
# Une colonne correctement typée permet ensuite de faire
# des opérations fiables sur les dates : extraction de l'année,
# tri chronologique, calcul de durée, filtrage par période, etc.
#
# errors="raise" est volontaire :
# si une date est invalide, Python arrête l'exécution au lieu
# de masquer silencieusement le problème.
#
# Nous avons déjà vérifié pendant la Data Quality que les
# 34 dates sont valides.

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="raise"
)

print("\nType de release_date après conversion :")
print(df["release_date"].dtype)
# ============================================================
# 3. CONTRÔLE APRÈS NETTOYAGE
# ============================================================

# On vérifie que la transformation n'a pas modifié la structure
# ou introduit de valeurs manquantes.
#
# Pourquoi ?
# Une transformation doit améliorer les données sans provoquer
# de perte ou de dégradation involontaire.

print("\nDimensions après nettoyage :", df.shape)

print("\nValeurs manquantes après nettoyage :")
print(df.isnull().sum().sum())
# ============================================================
# 4. EXPORT DES DONNÉES NETTOYÉES
# ============================================================

# On sauvegarde le DataFrame nettoyé dans un nouveau fichier CSV.
#
# Pourquoi ?
# On conserve la source originale intacte et on crée une
# nouvelle version destinée aux prochaines étapes du projet.
#
# index=False évite d'ajouter l'index Pandas comme une colonne
# supplémentaire dans le fichier CSV.

df.to_csv("marvel_movies_dataset_clean.csv", index=False)

print("\nFichier nettoyé créé avec succès.")