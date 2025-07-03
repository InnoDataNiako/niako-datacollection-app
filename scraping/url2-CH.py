import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base pour chaussures homme
base_url = "https://sn.coinafrique.com/categorie/chaussures-homme?page="
headers = {
    "User-Agent": "Mozilla/5.0"
}

data = []
nb_pages = 5  # Nombre de pages à scraper

for page in range(1, nb_pages + 1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur de requête sur la page {page}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    cards = soup.find_all("div", class_="card-content ad__card-content")

    for card in cards:
        try:
            # Type de chaussures
            type_chaussure = card.find("p", class_="ad__card-description").get_text(strip=True)

            # Prix
            prix = card.find("p", class_="ad__card-price").get_text(strip=True).replace("CFA", "").strip()

            # Adresse
            adresse = card.find("p", class_="ad__card-location").get_text(strip=True)

            # Image
            card_parent = card.find_parent("div", class_="card")
            img_tag = card_parent.find("img", class_="ad__card-img")
            image_lien = img_tag["src"] if img_tag else ""

            data.append({
                "type_chaussures": type_chaussure,
                "prix": prix,
                "adresse": adresse,
                "image_lien": image_lien
            })

        except Exception as e:
            print("Erreur de parsing :", e)
            continue

    time.sleep(1)

# DataFrame
df = pd.DataFrame(data)
print(df.head())

# Sauvegarde
df.to_csv("chaussures_homme.csv", index=False)
