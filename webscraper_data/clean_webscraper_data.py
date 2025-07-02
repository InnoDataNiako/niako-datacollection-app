import pandas as pd
import re
import os
import unicodedata
import urllib.parse

def nettoyer_dataframe(df, titre_col, etat_col, adresse_col, prix_col):
    df = df.copy()

    # Fonction pour nettoyer les titres (suppression de caractères indésirables)
    def clean_text(text):
        text = urllib.parse.unquote_plus(str(text))
        # Normalisation Unicode pour gérer les accents
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')  # Supprime les accents
        # Ou utiliser 'NFC' pour préserver les accents
        text = ''.join(c for c in text if c.isprintable() and not unicodedata.category(c).startswith('So'))
        text = re.sub(r'[\\\"\']', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # Nettoyage des titres
    df[titre_col] = df[titre_col].apply(clean_text)

    # Nettoyage des états (idem que tu avais)
    def map_condition(cond):
        cond = str(cond).lower()
        if "neuf" in cond:
            return "Neuf"
        elif "occasion" in cond:
            return "Occasion"
        elif "reconditionné" in cond:
            return "Reconditionné"
        elif "venant" in cond:
            return "Venant"
        return "Inconnu"
    df[etat_col] = df[etat_col].apply(map_condition)

    # Nettoyage spécifique des adresses : enlever les balises svg html et garder le texte
    def clean_adresse(adresse):
        adresse = str(adresse)
        # Supprimer tout ce qui est entre <svg ...>...</svg> (balise et contenu)
        adresse = re.sub(r'<svg.*?</svg>', '', adresse, flags=re.DOTALL)
        # Supprimer tout autre tag HTML s’il en reste (optionnel)
        adresse = re.sub(r'<.*?>', '', adresse)
        # Nettoyer les espaces en trop
        adresse = re.sub(r'\s+', ' ', adresse).strip()
        return adresse

    df[adresse_col] = df[adresse_col].apply(clean_adresse)

    # Nettoyage des prix (comme avant)
    def clean_price(price):
        try:
            return int(re.sub(r"[^\d]", "", str(price)))
        except:
            return None
    df[prix_col] = df[prix_col].apply(clean_price)

    return df


def traitement_webscraper(nom_fichier, colonnes):
    print(f"\n📥 Traitement de : {nom_fichier}")
    df = pd.read_excel(nom_fichier)

    df = nettoyer_dataframe(df, colonnes["V1"], colonnes["V2"], colonnes["V3"], colonnes["V4"])

   # Supprimer toutes les lignes avec valeurs manquantes dans au moins une colonne essentielle
    df = df.dropna(subset=[
        colonnes["V1"],  # titre
        colonnes["V2"],  # état
        colonnes["V3"],  # adresse
        colonnes["V4"]   # prix
    ])

    # Supprimer les doublons exacts
    df = df.drop_duplicates()

    # Supprimer aussi les doublons sur le titre + prix + adresse (s'il y a des copies)
    df = df.drop_duplicates(subset=[colonnes["V1"], colonnes["V3"], colonnes["V4"]])


    # Enregistrement dans le même dossier
    dossier = os.path.dirname(nom_fichier)
    clean_name = os.path.splitext(os.path.basename(nom_fichier))[0] + "_clean.csv"
    save_path = os.path.join(dossier, clean_name)
    df.to_csv(save_path, index=False, encoding="utf-8")
    print(f"✅ Enregistré : {save_path}")


def main():
    dossier = os.path.dirname(os.path.abspath(__file__))  # dossier actuel du script

    fichiers = {
        "ExpatDakarFrigos.xlsx": {
            "V1": "V1_détails",
            "V2": "V2_etat_frigo_cong",
            "V3": "V3_adresse",
            "V4": "V4_prix"
        },
        "ExpatDakarClimatisation.xlsx": {
            "V1": "V1_détails",
            "V2": "V2_etat_clim",
            "V3": "V3_adresse",
            "V4": "V4_prix"
        },
        "ExpatDakarCuisinieresFours.xlsx": {
            "V1": "V1_détails",
            "V2": "V2_cuisinieres-fours",
            "V3": "V3_adresse",
            "V4": "V4_prix"
        },
        "ExpatDakarMachinesLaver.xlsx": {
            "V1": "V1_détails",
            "V2": "V2_etat_machines_a_laver",
            "V3": "V3_adresse",
            "V4": "V4_prix"
        }
    }

    for fichier, colonnes in fichiers.items():
        chemin = os.path.join(dossier, fichier)
        if os.path.exists(chemin):
            traitement_webscraper(chemin, colonnes)
        else:
            print(f"❌ Fichier introuvable : {fichier}")

if __name__ == "__main__":
    main()
    
