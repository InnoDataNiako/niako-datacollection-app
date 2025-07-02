

# 📊 Streamlit Data Collection - Expat Dakar

Ce projet est une application interactive développée avec **Streamlit** pour scraper, explorer et visualiser des données 


##  Objectifs du projet

- Scraper les données de plusieurs catégories d'annonces (Réfrigérateurs, Climatisations, Fours, Machines à laver) avec **Selenium**.
- Télécharger des fichiers WebScraper (données non nettoyées).
- Afficher un dashboard interactif basé sur les données nettoyées.
- Intégrer un formulaire d’évaluation utilisateur.


##  Fonctionnalités de l'app

- 🔄 **Scraping via Selenium** : Sélection de catégorie et nombre de pages à scraper.
- 📥 **Téléchargement WebScraper** : Données récupérées via l’extension WebScraper.io (non nettoyées).
- 📊 **Dashboard dynamique** : Visualisation des données nettoyées sous forme de KPI, graphiques, analyses par ville et par marque.
- 📝 **Formulaire d’évaluation** : Pour recueillir des retours utilisateurs.


##  Technologies utilisées

- Python
- Streamlit
- Selenium
- Pandas
- Plotly
- WebScraper
- Git/GitHub


##  Lancer l'application localement

1. Cloner le dépôt :
git clone https://github.com/InnoDataNiako/first_app_streamlit_datacollection.git
cd first_app_streamlit_datacollection

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancer l'application :

```bash
streamlit run app.py
```

---

##  Déploiement

L'application peut être déployée facilement sur **Streamlit Community Cloud** ou tout autre service compatible.

Lien de l'app déployée : *(à insérer après déploiement)*

---

##  Structure du projet

```
📦 first_app_streamlit_datacollection
│
├── app.py                       # Fichier principal Streamlit
├── scraping/                   # Contient le code de scraping Selenium
│   └── scraper_selenium.py
├── webscraper_data/            # Données issues de WebScraper
├── cleaned_data/               # Données nettoyées
├── README.md                   # Ce fichier
└── requirements.txt            # Dépendances Python
```

---

##  Auteur

**Niako Kebe**
Étudiante passionnée de data science & développement.
📧 Contact : [drivenindata@gmail.com](mailto:drivenindata@gmail.com)

---

##  Remarques

* Le scraping peut prendre quelques minutes selon le nombre de pages choisies.
* Assurez-vous d’avoir une connexion internet pour accéder aux URLs du site.

---
