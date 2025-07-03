import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import os
import urllib.parse
import unicodedata

# 🔹 Fonction de nettoyage principale
def nettoyer_dataframe(df, col_type, col_adresse, col_prix):
    df = df.copy()

    # Nettoyage des colonnes textuelles (type & adresse)
    for col in [col_type, col_adresse]:
        df[col] = df[col].astype(str).apply(urllib.parse.unquote_plus)
        df[col] = df[col].apply(lambda x: ''.join(
            c for c in x if c.isprintable() and not unicodedata.category(c).startswith('So')
        ))
        df[col] = df[col].str.replace(r"[\"\'\\]", "", regex=True)
        df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)

    # Nettoyage du prix
    def clean_price(price):
        try:
            numeric_value = float(str(price).replace(" ", "").replace(",", ".").replace("CFA", ""))
            return int(numeric_value)
        except:
            return None

    df[col_prix] = df[col_prix].astype(str).apply(clean_price)
    df[col_prix] = df[col_prix].astype("Int64")  # Nullable integers

    return df

# 🔹 Traitement d'un seul fichier
def traitement_complet(nom_fichier, columns_map):
    print(f"\n➡️ Traitement de : {nom_fichier}")
    df = pd.read_csv(nom_fichier)

    # Garder uniquement les 4 colonnes
    df = df[list(columns_map.values())]

    col_type = columns_map["V1"]
    col_adresse = columns_map["V3"]
    col_prix = columns_map["V2"]

    df = nettoyer_dataframe(df, col_type, col_adresse, col_prix)

    # Suppression des lignes vides
    df = df.dropna(subset=[col_type])
    median_price = df[col_prix].median()
    df[col_prix] = df[col_prix].fillna(median_price)

    df = df.drop_duplicates()

    # Suppression des outliers
    Q1 = df[col_prix].quantile(0.25)
    Q3 = df[col_prix].quantile(0.75)
    IQR = Q3 - Q1
    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR
    df = df[(df[col_prix] >= low) & (df[col_prix] <= high)]

    # 📊 Visualisation rapide
    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df[col_prix], bins=30, kde=True)
    plt.title("Distribution des prix")

    plt.subplot(1, 2, 2)
    sns.countplot(y=df[col_adresse].value_counts().head(10).index)
    plt.title("Top 10 zones")

    plt.tight_layout()
    plt.savefig(nom_fichier.replace(".csv", "_visualisation.png"))
    plt.close()

    # ✅ Export
    nom_nettoye = nom_fichier.replace(".csv", "_clean.csv")
    df[col_prix] = df[col_prix].apply(lambda x: f"{x:,}".replace(",", " ") if pd.notnull(x) else x)
    df.to_csv(nom_nettoye, index=False, encoding="utf-8")
    print(f"✅ Données nettoyées enregistrées : {nom_nettoye}")

# 🔹 Menu terminal
def main():
    print("""
🎯 MENU DE NETTOYAGE CoinAfrique :
1. Vêtements Homme
2. Chaussures Homme
3. Vêtements Enfants
4. Chaussures Enfants
""")

    choix = input("Entrez votre choix (1 à 4) : ").strip()

    mapping = {
        "1": {
            "fichier": "coinafrique-vetements-homme.csv",
            "columns": {
                "V1": "V1_type_habits",
                "V2": "V2_prix",
                "V3": "V3_adresse",
                "V4": "V4_image_lien-src"
            }
        },
        "2": {
            "fichier": "coinafrique-chaussures-homme.csv",
            "columns": {
                "V1": "V1_type_chaussures",
                "V2": "V2_prix",
                "V3": "V3_adresse",
                "V4": "V4_image_lien-src"
            }
        },
        "3": {
            "fichier": "coinafrique-vetements-enfants.csv",
            "columns": {
                "V1": "V1_type_habits",
                "V2": "V2_prix",
                "V3": "V3_adresse",
                "V4": "V4_image_lien-src"
            }
        },
        "4": {
            "fichier": "coinafrique-chaussures-enfants.csv",  # nom avec faute corrigée ici
            "columns": {
                "V1": "V1_type_chaussures",
                "V2": "V2_prix",
                "V3": "V3_adresse",
                "V4": "V4_image_lien-src"
            }
        }
    }

    selection = mapping.get(choix)
    if selection and os.path.exists(selection["fichier"]):
        traitement_complet(selection["fichier"], selection["columns"])
    else:
        print("⚠️ Fichier introuvable ou choix invalide.")

if __name__ == "__main__":
    main()