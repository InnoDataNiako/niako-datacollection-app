import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base pour chaussures enfants
base_url = "https://sn.coinafrique.com/categorie/chaussures-enfants?page="
headers = {
    "User-Agent": "Mozilla/5.0"
}

data = []
nb_pages = 5  # ajuste selon ton besoin

for page in range(1, nb_pages + 1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur sur la page {page}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    cards = soup.find_all("div", class_="card-content ad__card-content")

    for card in cards:
        try:
            type_chaussure = card.find("p", class_="ad__card-description").get_text(strip=True)
            prix = card.find("p", class_="ad__card-price").get_text(strip=True).replace("CFA", "").strip()
            adresse = card.find("p", class_="ad__card-location").get_text(strip=True)

            parent_card = card.find_parent("div", class_="card")
            img_tag = parent_card.find("img", class_="ad__card-img")
            image_lien = img_tag["src"] if img_tag else ""

            data.append({
                "type_chaussures_enfant": type_chaussure,
                "prix": prix,
                "adresse": adresse,
                "image_lien": image_lien
            })

        except Exception as e:
            print("Erreur de parsing :", e)
            continue

    time.sleep(1)

# Export
df = pd.DataFrame(data)
df.to_csv("chaussures_enfants.csv", index=False)
print(df.head())
