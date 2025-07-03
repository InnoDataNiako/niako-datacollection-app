import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import os
import urllib.parse
import unicodedata

# Nettoyage principal
def nettoyer_dataframe(df, col_titre, col_adresse, col_prix):
    df = df.copy()

    # Nettoyage de texte : titre, adresse
    for col in [col_titre, col_adresse]:
        df[col] = df[col].astype(str).apply(urllib.parse.unquote_plus)
        df[col] = df[col].apply(lambda x: ''.join(
            c for c in x if c.isprintable() and not unicodedata.category(c).startswith('So')
        ))
        df[col] = df[col].str.replace(r"[\"\'\\]", "", regex=True)
        df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)

    # Nettoyage du prix
    def clean_price(price):
        try:
            # Supprimer les espaces, convertir en float, puis en int
            numeric_value = float(str(price).replace(" ", "").replace(",", "."))
            return int(numeric_value)
        except:
            return None

    df[col_prix] = df[col_prix].apply(clean_price)
    df[col_prix] = df[col_prix].astype("Int64")  # Pour permettre les valeurs nulles


    return df

# Traitement complet
def traitement_complet(nom_fichier, columns_map):
    print(f"\n Chargement de {nom_fichier}...")
    df = pd.read_csv(nom_fichier)

    titre = columns_map["V1"]
    adresse = columns_map["V3"]
    prix = columns_map["V2"]

    df = nettoyer_dataframe(df, titre, adresse, prix)

    print("\n Valeurs manquantes :")
    print(df.isnull().sum())

    df = df.dropna(subset=[titre])
    median_price = df[prix].median()
    df[prix] = df[prix].fillna(median_price)

    print("\n Doublons détectés :", df.duplicated().sum())
    df = df.drop_duplicates()

    # Suppression des prix anormaux (outliers)
    Q1 = df[prix].quantile(0.25)
    Q3 = df[prix].quantile(0.75)
    IQR = Q3 - Q1
    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR
    print(f"\n Suppression des valeurs < {low} ou > {high}")
    df = df[(df[prix] >= low) & (df[prix] <= high)]

    print("\n Statistiques des prix :")
    print(df[prix].describe())

    # Graphiques
    plt.figure(figsize=(14, 5))

    plt.subplot(1, 2, 1)
    sns.histplot(df[prix], bins=30, kde=True)
    plt.title("Distribution des prix")

    plt.subplot(1, 2, 2)
    sns.countplot(y=df[adresse].value_counts().head(10).index)
    plt.title("Top 10 des zones")

    plt.tight_layout()
    plt.savefig("coin_clean_visualisation.png")
    plt.close()

    # Export
    nom_nettoye = nom_fichier.replace(".csv", "_clean.csv")
    df[prix] = df[prix].apply(lambda x: f"{x:,}".replace(",", " ") if pd.notnull(x) else x)
    df.to_csv(nom_nettoye, index=False, encoding="utf-8")
    print(f"\n Fichier nettoyé enregistré sous : {nom_nettoye}")

# Menu terminal
def main():
    print("""
 MENU DE NETTOYAGE CoinAfrique :
1. Vêtements Homme
2. Chaussures Homme
3. Vêtements Enfants
4. Chaussures Enfants
""")

    choix = input(" Entrez votre choix (1 à 4) : ").strip()

    mapping = {
        "1": {
            "fichier": "Vêtements_homme.csv",
            "columns": {
                "V1": "type_habits",
                "V2": "prix",
                "V3": "adresse",
                "V4": "image_lien"
            }
        },
        "2": {
            "fichier": "chaussures_homme.csv",
            "columns": {
                "V1": "type_chaussures",
                "V2": "prix",
                "V3": "adresse",
                "V4": "image_lien"
            }
        },
        "3": {
            "fichier": "Vêtements_enfants.csv",
            "columns": {
                "V1": "type_habits_enfant",
                "V2": "prix",
                "V3": "adresse",
                "V4": "image_lien"
            }
        },
        "4": {
            "fichier": "chaussures_enfants.csv",
            "columns": {
                "V1": "type_chaussures_enfant",
                "V2": "prix",
                "V3": "adresse",
                "V4": "image_lien"
            }
        }
    }

    selection = mapping.get(choix)
    if selection and os.path.exists(selection["fichier"]):
        traitement_complet(selection["fichier"], selection["columns"])
    else:
        print(" Fichier introuvable ou choix invalide.")

if __name__ == "__main__":
    main()
