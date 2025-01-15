import pandas as pd
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Charger le jeu de données Titanic
titanic_df = pd.read_csv('C:\\BI\\titanic.csv')

# 1. Combien de valeurs manquantes existe-t-il dans chaque colonne ?
missing_values = titanic_df.isnull().sum()
print("Valeurs manquantes par colonne :")
print(missing_values)

# 2. Remplissez les valeurs manquantes de la colonne Age avec sa médiane.
titanic_df['Age'].fillna(titanic_df['Age'].median(), inplace=True)

# 3. Remplissez les valeurs manquantes de la colonne Embarked avec sa valeur la plus fréquente.
most_frequent_embarked = titanic_df['Embarked'].mode()[0]
titanic_df['Embarked'].fillna(most_frequent_embarked, inplace=True)

# 4. Combien de lignes sont supprimées après la suppression des lignes contenant des valeurs manquantes dans les colonnes Cabin et Ticket ?
initial_rows = titanic_df.shape[0]
titanic_df_dropped = titanic_df.dropna(subset=['Cabin', 'Ticket'])
rows_dropped = initial_rows - titanic_df_dropped.shape[0]
print(f"Lignes supprimées après suppression : {rows_dropped}")

# 5. Extraire les titres de la colonne Name et les enregistrer dans une nouvelle colonne Title.
titanic_df['Title'] = titanic_df['Name'].apply(lambda x: re.search(r'\b(Mr|Mrs|Miss|Master|Dr|Rev|Col|Major|Capt|Countess|Lady|Sir|Don|Dona)\b', x).group() if re.search(r'\b(Mr|Mrs|Miss|Master|Dr|Rev|Col|Major|Capt|Countess|Lady|Sir|Don|Dona)\b', x) else 'Other')

# Supprimer les titres de la colonne Name.
titanic_df['Name'] = titanic_df['Name'].apply(lambda x: re.sub(r'\b(Mr|Mrs|Miss|Master|Dr|Rev|Col|Major|Capt|Countess|Lady|Sir|Don|Dona)\b', '', x).strip())

# 6. Convertir la colonne Sex en valeurs numériques (0 pour homme et 1 pour femme).
titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})

# 7. Convertir la colonne Embarked en valeurs numériques :
# 0 pour Cherbourg (C), 1 pour Queenstown (Q), 2 pour Southampton (S).
titanic_df['Embarked'] = titanic_df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})

# 8. Utilisez le fuzzy matching pour identifier les doublons approximatifs dans la colonne Name.
names = titanic_df['Name'].tolist()
duplicates = []

for i in range(len(names)):
    for j in range(i + 1, len(names)):
        score = fuzz.ratio(names[i], names[j])
        if score >= 90:  # Seuil de similarité de 90
            duplicates.append((names[i], names[j], score))

# Trier les doublons par score de similarité
duplicates_sorted = sorted(duplicates, key=lambda x: x[2], reverse=True)

# Afficher les paires de noms similaires ayant un score de similarité supérieur ou égal à 90
print("Paires de noms similaires :")
for pair in duplicates_sorted:
    print(f"Nom 1: {pair[0]} | Nom 2: {pair[1]} | Score de similarité: {pair[2]}")
