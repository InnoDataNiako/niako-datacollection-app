# scraping/scraper_4url_BS.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime
import unicodedata

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text.lower().replace(" ", "_").replace("&", "et")

def scrape_category(url, file_path, column_map, max_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = []

    for page in range(1, max_pages + 1):
        page_url = f"{url}?page={page}"
        print(f"Scraping {page_url}")
        try:
            response = requests.get(page_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Erreur page {page}: Code {response.status_code}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.find_all("div", class_="card-content ad__card-content")

            if not cards:
                print(f"Aucune annonce trouvée sur la page {page}")
                continue

            for card in cards:
                try:
                    type_prod = card.find("p", class_="ad__card-description").get_text(strip=True)
                    prix = card.find("p", class_="ad__card-price").get_text(strip=True).replace("CFA", "").replace(" ", "").strip()
                    adresse = card.find("p", class_="ad__card-location").get_text(strip=True)
                    parent = card.find_parent("div", class_="card")
                    img_tag = parent.find("img", class_="ad__card-img")
                    image_lien = img_tag["src"] if img_tag else ""

                    # Map the scraped data to the specified column names
                    data.append({
                        column_map["V1"]: type_prod,
                        column_map["V2"]: prix,
                        column_map["V3"]: adresse,
                        column_map["V4"]: image_lien
                    })

                except Exception as e:
                    print(f"Erreur de parsing sur la page {page}: {e}")
                    continue

            time.sleep(1)  # Respectful delay to avoid overloading the server

        except Exception as e:
            print(f"Erreur lors de la requête pour la page {page}: {e}")
            continue

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    if not df.empty:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Données exportées dans : {file_path}")
    else:
        print("Aucune donnée collectée.")

    return df

# Categories configuration for reference
categories = {
    "Vêtements Homme": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "column_map": {
            "V1": "type_habits",
            "V2": "prix",
            "V3": "adresse",
            "V4": "image_lien"
        },
        "icon": "👔"
    },
    "Chaussures Homme": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "column_map": {
            "V1": "type_chaussures",
            "V2": "prix",
            "V3": "adresse",
            "V4": "image_lien"
        },
        "icon": "👞"
    },
    "Vêtements Enfants": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "column_map": {
            "V1": "type_habits",
            "V2": "prix",
            "V3": "adresse",
            "V4": "image_lien"
        },
        "icon": "👕"
    },
    "Chaussures Enfants": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "column_map": {
            "V1": "type_chaussures",
            "V2": "prix",
            "V3": "adresse",
            "V4": "image_lien"
        },
        "icon": "👟"
    }
}
# ...existing code...

if __name__ == "__main__":
    print("=== MENU SCRAPING COINAFRIQUE ===")
    print("Catégories disponibles :")
    for i, cat in enumerate(categories.keys(), 1):
        print(f"{i}. {cat}")

    choix = input("Entrez le numéro de la catégorie à scraper : ")
    try:
        choix = int(choix)
        cat_name = list(categories.keys())[choix - 1]
    except (ValueError, IndexError):
        print("Numéro invalide.")
        exit(1)

    max_pages = input("Nombre de pages à scraper (défaut 5) : ")
    try:
        max_pages = int(max_pages)
    except ValueError:
        max_pages = 5

    config = categories[cat_name]
    slug = slugify(cat_name)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"coinafrique_{slug}_{now}.csv"

    print(f"Lancement du scraping pour '{cat_name}' sur {max_pages} pages...")
    df = scrape_category(config["url"], file_path, config["column_map"], max_pages=max_pages)
    if not df.empty:
        print(f"Scraping terminé. Fichier sauvegardé : {file_path}")
    else:
        print("Aucune donnée collectée.")