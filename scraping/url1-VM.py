import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuration de base
base_url = "https://sn.coinafrique.com/categorie/vetements-homme?page="
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Stockage des résultats
data = []

# Nombre de pages à scraper (tu peux ajuster selon le site)
nb_pages = 5  # par exemple 5 pages

for page in range(1, nb_pages + 1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Erreur lors de la requête pour la page {page}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    cards = soup.find_all("div", class_="card-content ad__card-content")

    for card in cards:
        try:
            # Type (titre du produit)
            type_produit = card.find("p", class_="ad__card-description").get_text(strip=True)

            # Prix
            prix = card.find("p", class_="ad__card-price").get_text(strip=True).replace("CFA", "").strip()

            # Adresse
            adresse = card.find("p", class_="ad__card-location").get_text(strip=True)

            # Image (on va chercher le parent div avec classe card pour remonter au lien image)
            card_parent = card.find_parent("div", class_="card")
            img_tag = card_parent.find("img", class_="ad__card-img")
            image_lien = img_tag["src"] if img_tag else ""

            data.append({
                "type_habits": type_produit,
                "prix": prix,
                "adresse": adresse,
                "image_lien": image_lien
            })

        except Exception as e:
            print("Erreur sur une carte:", e)
            continue

    time.sleep(1)  # Pause pour éviter d'être bloqué

# Convertir en DataFrame
df = pd.DataFrame(data)
print(df.head())

# Sauvegarde CSV
df.to_csv("vetements_homme.csv", index=False)
