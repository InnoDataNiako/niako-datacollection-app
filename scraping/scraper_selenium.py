
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import unicodedata
import os
import random
import json
from fake_useragent import UserAgent

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


def scrape_category(base_url, csv_filename, column_map, max_pages=20):
    listings_data = []
    
    # Configuration des headers avec User-Agent aléatoire
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }

    session = requests.Session()
    session.headers.update(headers)

    for page in range(1, max_pages + 1):
        try:
            # Délai aléatoire plus long avec variation
            delay = random.uniform(3.0, 7.0)
            time.sleep(delay)
            
            # Rotation des headers à chaque requête
            session.headers.update({"User-Agent": ua.random})
            
            url = f"{base_url}?page={page}" if page > 1 else base_url
            print(f"Tentative de scraping: {url}")
            
            # Ajout de paramètres aléatoires pour éviter le cache
            params = {"_": str(int(time.time()))} if page > 1 else {}
            
            resp = session.get(url, params=params, timeout=30)
            
            # Vérification du statut
            if resp.status_code == 403:
                print("Accès refusé (403 Forbidden) - Essayez plus tard ou changez d'IP")
                break
            resp.raise_for_status()
            
            # Vérification contenu minimal
            if len(resp.text) < 2000:
                print(f"Contenu insuffisant page {page}")
                continue
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Extraction avec les sélecteurs exacts fournis
            cards = soup.select("div.listing-card__inner")
            print(f"Nombre d'annonces trouvées: {len(cards)}")
            
            for card in cards:
                try:
                    data = {
                        column_map["V1"]: clean_text(card.select_one('div.listing-card__header__title').text) if card.select_one('div.listing-card__header__title') else "N/A",
                        column_map["V2"]: clean_text(card.select_one('span.listing-card__header__tags__item').text) if card.select_one('span.listing-card__header__tags__item') else "N/A",
                        column_map["V3"]: clean_text(card.select_one('div.listing-card__header__location').text) if card.select_one('div.listing-card__header__location') else "N/A",
                        column_map["V4"]: clean_text(card.select_one('span.listing-card__price__value').text) if card.select_one('span.listing-card__price__value') else "N/A",
                        column_map["V5"]: card.select_one('img.listing-card__image__resource')['src'] if card.select_one('img.listing-card__image__resource') else "N/A",
                        "Page": page
                    }
                    listings_data.append(data)
                    
                except Exception as e:
                    print(f"Erreur sur une annonce: {str(e)}")
                    continue
                    
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau page {page}: {str(e)}")
            continue
        except Exception as e:
            print(f"Erreur inattendue page {page}: {str(e)}")
            continue

    # Création du DataFrame et sauvegarde
    df = pd.DataFrame(listings_data)
    if not df.empty:
        try:
            os.makedirs(os.path.dirname(csv_filename) or '.', exist_ok=True)
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"Sauvegarde réussie dans {csv_filename}")
        except Exception as e:
            print(f"Erreur sauvegarde CSV: {str(e)}")
    
    return df