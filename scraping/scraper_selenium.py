import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

def scrape_category(base_url, csv_filename, column_map, max_pages=20):
    listings_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        print(f"Scraping page {page}: {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"Erreur lors du chargement de la page {page}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", class_="listing-card__inner")
        print(f"Nombre de cartes trouvées : {len(cards)}")

        for i, card in enumerate(cards, 1):
            try:
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
                print(f"Données extraites pour la carte {i} sur la page {page}: {title}")
            except Exception as card_error:
                print(f"Erreur sur la carte {i} de la page {page}: {str(card_error)}")
                continue

        time.sleep(1)

    df = pd.DataFrame(listings_data)
    if os.path.dirname(csv_filename):
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    return df