import streamlit as st
import os
import pandas as pd
from datetime import datetime
from scraping.scraper_4url_BS import scrape_category
import unicodedata
import plotly.express as px
import tempfile

# Partie 2: Configuration de la page et du style
st.set_page_config(page_title="CoinAfrique", layout="wide")

# Partie 3: CSS pour le style de la sidebar et des cartes
st.markdown("""
    <style>
    /* Fond noir pour la sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: #ffffff;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        padding: 20px 10px 10px 10px;
        border-bottom: 1px solid #374151;
    }
    .search-box {
        margin-top: 10px;
        margin-bottom: 20px;
        padding: 0 10px;
    }
    div[role="radiogroup"] > label {
        color: #f3f4f6;
        padding: 10px;
        border-radius: 8px;
        margin: 4px 10px;
        display: flex;
        align-items: center;
        font-size: 16px;
        font-weight: 500;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #1f2937;
        cursor: pointer;
    }
    hr {
        border: none;
        border-top: 1px solid #374151;
        margin: 10px 10px;
    }
    .centered-title {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Partie 4: Titre de la sidebar et menu principal
st.sidebar.markdown('<div class="sidebar-title">📦 CoinAfrique</div>', unsafe_allow_html=True)
menu = st.sidebar.radio("Fonctionnalité Principale", [
    "🔄 Scraper les données",
    "📥 Télécharger WebScraper",
    "📊 Dashboard Données Nettoyées",
    "📝 Formulaire d'évaluation",
])

# Partie 5: Affichage du titre principal en fonction du menu sélectionné
if menu == "🔄 Scraper les données":
    st.markdown("<h1 class='centered-title'>Scraper avec BeautifulSoup</h1>", unsafe_allow_html=True)
elif menu == "📥 Télécharger WebScraper":
    st.markdown("""
    <div class="download-card">
        <div class="download-header">
            <h2 class="download-title">Télécharger les données WebScraper</h2>
        </div>
        <p style="color: #6b7280; margin-bottom: 20px;">
            Sélectionnez les fichiers CSV à télécharger. Ces fichiers contiennent les données déjà scrapées (non nettoyées).
        </p>
    </div>
    """, unsafe_allow_html=True)
elif menu == "📊 Dashboard Données Nettoyées":
    st.markdown("<h1 class='centered-title'>Dashboard Données Nettoyées</h1>", unsafe_allow_html=True)
elif menu == "📝 Formulaire d'évaluation":
    st.markdown('<div class="form-title">📝 Formulaire d\'Évaluation</div>', unsafe_allow_html=True)

# Partie 6: Scraping avec BeautifulSoup
if menu == "🔄 Scraper les données":
    st.markdown("""
    <div class="scraping-card" style="margin-top: 20px;">
        <p>Choisissez une catégorie et le nombre de pages à scraper sur <a href="https://sn.coinafrique.com/" target="_blank">coinafrique.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="scraping-card">', unsafe_allow_html=True)
        
        categories = {
            "Vêtements Homme": {
                "url": "https://sn.coinafrique.com/categorie/vetements-homme",
                "column_map": {
                    "V1": "type_habits",
                    "V2": "prix",
                    "V3": "adresse",
                    "V4": "image_lien"
                },
                "icon": "👔" 
            },  
            "Chaussures Homme": {
                "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
                "column_map": {
                    "V1": "type_chaussures",
                    "V2": "prix",
                    "V3": "adresse",
                    "V4": "image_lien"
                },
                "icon": "👟"
            },
            "Vêtements Enfants": {
                "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
                "column_map": {
                    "V1": "type_habits",
                    "V2": "prix",
                    "V3": "adresse",
                    "V4": "image_lien"
                },
                "icon": "👕"
            },
            "Chaussures Enfants": {
                "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
                "column_map": {
                    "V1": "type_chaussures_enfants",
                    "V2": "prix",
                    "V3": "adresse",
                    "V4": "image_lien"
                },
                "icon": "👟"
            }
        }   

        category = st.selectbox("Sélectionnez une catégorie", list(categories.keys()), format_func=lambda x: f"{categories[x]['icon']} {x}")
        num_pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=100, value=5, step=1)
        st.markdown('</div>', unsafe_allow_html=True)
        # Partie 9 : Bouton pour lancer le scraping
        if st.button("🚀 Lancer le scraping", key="scrape_button"):
            with st.spinner("🔄 Scraping en cours... Cette opération peut prendre quelques minutes."):
                try:
                    def slugify(text):
                        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
                        return text.lower().replace(" ", "_").replace("&", "et")

                    filename_base = slugify(category)
                    csv_filename = f"{filename_base}_{num_pages}-pages_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

                    # Créer un fichier temporaire dans le même processus
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                    file_path = tmp_file.name
                    tmp_file.close()  # important pour qu'on puisse l'ouvrir plus tard

                    config = categories[category]
                    df = scrape_category(config["url"], file_path, config["column_map"], max_pages=num_pages)

                    if df is not None and os.path.exists(file_path):
                        st.markdown(f"""
                        <div class="scraping-card stSuccess">
                            <div class="section-title">✅ Scraping terminé avec succès</div>
                            <p>Données extraites pour la catégorie <strong>{category}</strong> sur <strong>{num_pages}</strong> pages.</p>
                            <p>Fichier généré : <code>{file_path}</code></p>
                        </div>
                        """, unsafe_allow_html=True)

                        with open(file_path, "rb") as file:
                            st.download_button(
                                label=f"📥 Télécharger {csv_filename}",
                                data=file,
                                file_name=csv_filename,
                                mime="text/csv",
                                key="download_csv"
                            )
                        # Facultatif : supprimer le fichier après
                        # os.remove(file_path)
                    else:
                        st.markdown("""
                        <div class="scraping-card stError">
                            <div class="section-title">❌ Erreur</div>
                            <p>Le fichier scrapé n'a pas pu être trouvé ou est vide.</p>
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f"""
                    <div class="scraping-card stError">
                        <div class="section-title">❌ Erreur pendant le scraping</div>
                        <p>Une erreur s'est produite :</p>
                        <code>{str(e)}</code>
                    </div>
                    """, unsafe_allow_html=True)

# Partie 10 : si le menu sélectionné est "Télécharger WebScraper "
elif menu == "📥 Télécharger WebScraper":
    st.markdown("""
    <style>
        .download-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #4f46e5;
        }
        .download-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        }
        .download-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .download-icon {
            font-size: 24px;
            margin-right: 12px;
            color: #4f46e5;
        }
        .download-title {
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            margin: 0;
        }
        .download-btn {
            background-color: #4f46e5 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            border: none !important;
        }
        .download-btn:hover {
            background-color: #4338ca !important;
        }
        .warning-card {
            background: #fff3f3;
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Partie 11 : Affichage des fichiers disponibles pour téléchargement
    dossier_csv = "webscraper_data"
    fichiers = {
        "👔 Vêtements Homme": "coinafrique-vetements-homme.csv",
        "👟 Chaussures Homme": "coinafrique-chaussures-homme.csv",
        "👕 Vêtements Enfants": "coinafrique-vetements-enfants.csv",
        "👟 Chaussures Enfants": "coinafrique-chaussures-enfants.csv"
    }
# Partie 12 : Vérification de l'existence des fichiers et affichage des boutons de téléchargement
    for nom, fichier in fichiers.items():
        chemin = os.path.join(dossier_csv, fichier)
        if os.path.exists(chemin):
            with st.container():
                st.markdown(f"""
                <div class="download-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0 0 5px 0; color: #1f2937;">{nom.split()[1]}</h3>
                            <p style="margin: 0; color: #6b7280; font-size: 14px;">{fichier}</p>
                        </div>
                """, unsafe_allow_html=True)
                
                with open(chemin, "rb") as f:
                    st.download_button(
                        label=f"Télécharger",
                        data=f,
                        file_name=fichier,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"dl_{fichier}",
                        help=f"Télécharger le fichier {fichier}"
                    )
                
                st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">⚠️</span>
                    <div>
                        <strong style="color: #ef4444;">Fichier manquant</strong>
                        <p style="margin: 5px 0 0 0; color: #6b7280;">{fichier} n'a pas été trouvé dans le dossier {dossier_csv}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
