import json
import pandas as pd
import matplotlib.pyplot as plt

with open("C:/Users/dell/Downloads/evg_esp_veg.envpdiprboucle.json", "r", encoding="utf-8") as f:
    d_json = json.load(f)

print("Fichier chargé avec succès !")
print(type(d_json))
print(d_json.keys())


print("\n--- Question 1.2 ---")

# Les clés du dictionnaire
print("Clés du JSON :", d_json.keys())

# Liste des champs (noms des colonnes)
print("\nListe des champs (fields) :")
print(d_json["fields"])

# Liste des randonnées (les lignes du tableau)
print("\nExemple d'une randonnée (ligne 0) :")
print(d_json["values"][0])

print("\n--- Question 1.3 ---")

var = d_json["fields"]     # liste des champs
rando = d_json["values"]   # liste des randonnées

print("Nombre de champs :", len(var))
print("Nombre de randonnées :", len(rando))

print("\nPremier champ :", var[0])
print("Première randonnée :", rando[0])


print("\n--- Question 1.4 ---")
print("Taille du jeu (nb de lignes) :", len(rando))

# 1.2 – Récupération des champs et des randonnées
fields = d_json["fields"]
values = d_json["values"]

print("\n--- Question 2.1 ---")

df = pd.DataFrame(values, columns=fields)
print(df.head())
print(df.info())

print(df.columns)


print("\n--- 2.2 : Aperçu début / fin ---")
print("Début :")
print(df.head())

print("\nFin :")
print(df.tail())

print("\n--- 2.3 : iloc / loc ---")

# iloc : index numériques [lignes, colonnes]
print("\nColonnes 1 à 4 (par index) :")
print(df.iloc[:, 1:4])   # colonnes 1,2,3

# loc : par noms de colonnes
print("\nColonnes 'nom' et 'difficulte' :")
print(df.loc[:, ["nom", "difficulte"]])

# Exemple de modification avec loc (juste pour illustration)
# Ici on met la difficulté en minuscule
df.loc[:, "difficulte"] = df["difficulte"].str.lower()
print("\nDifficultés après passage en minuscules :")
print(df["difficulte"].value_counts())
