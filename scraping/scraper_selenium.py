import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from random import uniform

def scrape_category(base_url, csv_filename, column_map, max_pages=20):
    listings_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        print(f"Scraping page {page}: {url}")
        
        try:
            # Délai aléatoire anti-blocage (1-3 secondes)
            time.sleep(uniform(1.0, 3.0))
            
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            # Vérification rapide du contenu
            if len(resp.text) < 1000:
                print(f"Contenu anormalement court pour la page {page}")
                continue
                
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau sur la page {page}: {e}")
            continue
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", class_="listing-card__inner")
        print(f"Cartes trouvées: {len(cards)}")

        for i, card in enumerate(cards, 1):
            try:
                # Vos sélecteurs originaux exacts
                title = card.find("div", class_="listing-card__header__title")
                title = title.get_text(strip=True) if title else "N/A"

                condition = card.select_one(".listing-card__header__tags__item--condition")
                condition = condition.get_text(strip=True) if condition else "N/A"

                address = card.find("div", class_="listing-card__header__location")
                address = address.get_text(strip=True) if address else "N/A"

                price = card.find("div", class_="listing-card__price__deal")
                if not price:
                    price = card.find("div", class_="listing-card__price__value")
                price = price.get_text(strip=True) if price else "N/A"

                image = card.find("img", class_="listing-card__image__resource")
                image = image["src"] if image and image.has_attr("src") else "N/A"

                listings_data.append({
                    column_map["V1"]: title,
                    column_map["V2"]: condition,
                    column_map["V3"]: address,
                    column_map["V4"]: price,
                    column_map["V5"]: image,
                    "Page": page
                })
                
            except Exception as card_error:
                print(f"Erreur carte {i}: {card_error}")
                continue

    if not listings_data:
        print("Aucune donnée collectée")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(listings_data)
        os.makedirs(os.path.dirname(csv_filename) or ".", exist_ok=True)
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        return df
    except Exception as e:
        print(f"Erreur création CSV: {e}")
        return pd.DataFrame()