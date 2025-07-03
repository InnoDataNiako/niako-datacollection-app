# 📊 Streamlit Data Collection - CoinAfrique

Ce projet est une application interactive développée avec **Streamlit** pour scraper, explorer et visualiser des données issues du site **CoinAfrique**.

## Objectifs du projet

- Scraper les données de plusieurs catégories d'annonces (Vêtements Homme, Chaussures Homme, Vêtements Enfants, Chaussures Enfants) avec **BeautifulSoup**.
- Télécharger des fichiers WebScraper (données non nettoyées).
- Afficher un dashboard interactif basé sur les données nettoyées.
- Intégrer un formulaire d’évaluation utilisateur.

## Fonctionnalités de l'app

- 🔄 **Scraping via BeautifulSoup** : Sélection de catégorie et nombre de pages à scraper.
- 📥 **Téléchargement WebScraper** : Données récupérées via l’extension WebScraper.io (non nettoyées).
- 📊 **Dashboard dynamique** : Visualisation des données nettoyées sous forme de KPI, graphiques, analyses par ville et par type.
- 📝 **Formulaire d’évaluation** : Pour recueillir des retours utilisateurs.

## Technologies utilisées

- Python
- Streamlit
- BeautifulSoup
- Pandas
- Plotly
- WebScraper
- Git/GitHub

## Lancer l'application localement

1. Cloner le dépôt :
```bash
git clone https://github.com/InnoDataNiako/first_app_streamlit_datacollection.git
cd first_app_streamlit_datacollection
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancer l'application :

```bash
streamlit run app.py
```

---

## Déploiement

L'application peut être déployée facilement sur **Streamlit Community Cloud** ou tout autre service compatible.

Lien de l'app déployée : *https://niako-datacollection-app.streamlit.app/*

---

## Structure du projet

```
📦 niako-datacollection-app
│
├── app.py                       # Fichier principal Streamlit
├── scraping/                    # Contient le code de scraping BeautifulSoup
│   └── scraper_4url_BS.py
├── webscraper_data/             # Données issues de WebScraper
├── cleaned_data/                # Données nettoyées
├── README.md                    # Ce fichier
└── requirements.txt             # Dépendances Python
```

---

## Auteur

**Niako Kebe**  
Étudiante passionnée de data science & développement.  
📧 Contact : [drivenindata@gmail.com](mailto:drivenindata@gmail.com)

---

## Remarques

* Le scraping peut prendre quelques minutes selon le nombre de pages choisies.
* Assurez-vous d’avoir une connexion internet pour accéder aux URLs du site.

---