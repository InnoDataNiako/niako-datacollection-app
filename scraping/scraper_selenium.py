
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import unicodedata

# Liste des URLs avec leurs catégories
urls = [
    {"url": "https://www.expat-dakar.com/refrigerateurs-congelateurs", "category": "Réfrigérateurs-Congélateurs", "etat_label": "État Frigo-Cong"},
    {"url": "https://www.expat-dakar.com/climatisation", "category": "Climatisation", "etat_label": "État Clim"},
    {"url": "https://www.expat-dakar.com/cuisinieres-fours", "category": "Cuisinières-Fours", "etat_label": "État Cuisinière"},
    {"url": "https://www.expat-dakar.com/machines-a-laver", "category": "Machines à laver", "etat_label": "État Machine"}
]

# Sélecteurs CSS communs
selectors = {
    "details": "div.listing-card__header__title",
    "etat": "span.listing-card__header__tags__item",
    "adresse": "div.listing-card__header__location",
    "prix": "span.listing-card__price__value",
    "image_lien": "img.listing-card__image__resource"
}

# Liste pour stocker toutes les données
all_data = []

# Fonction pour nettoyer le texte
def clean_text(text):
    return ' '.join(text.split()) if text else ''

# Fonction pour scraper une page
def scraper_categorie(url, category, etat_label, page_num):
    try:
        response = requests.get(f"{url}?page={page_num}", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver toutes les cartes de produits
        listings = soup.select("div.listing-card")
        
        for listing in listings:
            # Extraction des données avec gestion des erreurs
            details = clean_text(listing.select_one(selectors["details"]).get_text(strip=True) if listing.select_one(selectors["details"]) else '')
            etat = clean_text(listing.select_one(selectors["etat"]).get_text(strip=True) if listing.select_one(selectors["etat"]) else '')
            adresse = clean_text(listing.select_one(selectors["adresse"]).get_text(strip=True) if listing.select_one(selectors["adresse"]) else '')
            prix = clean_text(listing.select_one(selectors["prix"]).get_text(strip=True) if listing.select_one(selectors["prix"]) else '')
            image_lien = urljoin(url, listing.select_one(selectors["image_lien"])['src'] if listing.select_one(selectors["image_lien"]) and 'src' in listing.select_one(selectors["image_lien"]).attrs else '')
            
            # Ajouter les données à la liste
            all_data.append({
                "Catégorie": category,
                "Détails": details,
                etat_label: etat,
                "Adresse": adresse,
                "Prix": prix,
                "Image_Lien": image_lien
            })
        
        # Vérifier s'il y a une page suivante
        next_page = soup.select_one("a[rel='next']")
        return bool(next_page)
    
    except requests.RequestException as e:
        print(f"Erreur lors de la requête pour {url}?page={page_num}: {e}")
        return False

# Parcourir chaque URL
for item in urls:
    url = item["url"]
    category = item["category"]
    etat_label = item["etat_label"]
    page_num = 1
    
    print(f"Scraping {category}...")
    while True:
        has_next = scraper_categorie(url, category, etat_label, page_num)
        print(f"Page {page_num} scraped for {category}")
        page_num += 1
        if not has_next:
            break
        time.sleep(2)  # Pause pour éviter de surcharger le serveur
    
    # Sauvegarder les données après chaque catégorie
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(f"{category.lower().replace(' ', '_')}_data.csv", index=False, encoding='utf-8')
        print(f"Données sauvegardées pour {category} dans {category.lower().replace(' ', '_')}_data.csv")

# Sauvegarder toutes les données dans un fichier final
if all_data:
    final_df = pd.DataFrame(all_data)
    final_df.to_csv("all_products_data.csv", index=False, encoding='utf-8')
    print("Toutes les données ont été sauvegardées dans all_products_data.csv")