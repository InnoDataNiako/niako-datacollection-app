import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import streamlit as st
from random import uniform
# Scraper pour une catégorie spécifique
# Utilise BeautifulSoup pour extraire les données des cartes de listing
def scrape_category(base_url, csv_filename, column_map, max_pages=20):
    listings_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Referer": "https://www.google.com/"
    }

    for page in range(1, max_pages + 1):
        try:
            # Délai aléatoire avec progression
            time.sleep(max(1, uniform(1.0, 3.0)))
            
            url = f"{base_url}?page={page}" if page > 1 else base_url
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.find_all("div", class_="listing-card__inner")
            
            if not cards and page == 1:
                st.warning("Aucune donnée trouvée - vérifiez les sélecteurs")
                return pd.DataFrame()
                
            for card in cards:
                try:
                    data = {
                        column_map["V1"]: card.find("div", class_="listing-card__header__title").get_text(strip=True) if card.find("div", class_="listing-card__header__title") else "N/A",
                        column_map["V2"]: card.select_one(".listing-card__header__tags__item--condition").get_text(strip=True) if card.select_one(".listing-card__header__tags__item--condition") else "N/A",
                        column_map["V3"]: card.find("div", class_="listing-card__header__location").get_text(strip=True) if card.find("div", class_="listing-card__header__location") else "N/A",
                        column_map["V4"]: (card.find("div", class_="listing-card__price__deal") or card.find("div", class_="listing-card__price__value")).get_text(strip=True) if (card.find("div", class_="listing-card__price__deal") or card.find("div", class_="listing-card__price__value")) else "N/A",
                        column_map["V5"]: card.find("img", class_="listing-card__image__resource")["src"] if card.find("img", class_="listing-card__image__resource") and card.find("img", class_="listing-card__image__resource").has_attr("src") else "N/A",
                        "Page": page
                    }
                    listings_data.append(data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            continue

    df = pd.DataFrame(listings_data)
    if not df.empty:
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')  # utf-8-sig pour Excel
    return df