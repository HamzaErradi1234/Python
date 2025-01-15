import pandas as pd

# 1
sf_permits = pd.read_csv('C:\\BI\\Building_Permits.csv')

# 2
print(sf_permits.head())

# 3
print(sf_permits.isnull().sum().sum())

# 4
missing_percentage = (sf_permits.isnull().sum().sum() / sf_permits.size) * 100
print(f"Pourcentage de valeurs manquantes : {missing_percentage:.2f}%")

# 5
sf_permits_dropped_rows = sf_permits.dropna()
print(f"Nombre de lignes restantes après suppression : {sf_permits_dropped_rows.shape[0]}")

# 6
# a
sf_permits_with_na_dropped = sf_permits.dropna(axis=1)
print(f"Nombre de colonnes supprimées : {sf_permits.shape[1] - sf_permits_with_na_dropped.shape[1]}")

# 7
# a
sf_permits_with_na_imputed = sf_permits.bfill().fillna(0)
print(sf_permits_with_na_imputed.head())
print(sf_permits_with_na_imputed.isnull().sum())