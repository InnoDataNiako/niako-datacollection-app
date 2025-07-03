import streamlit as st
import os
import pandas as pd
from datetime import datetime
from scraping.scraper_4url_BS import scrape_category
import unicodedata
import plotly.express as px
import tempfile
import re
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
Sélectionnez les fichiers CSV à télécharger. Ces fichiers contiennent les données brutes collectées.        </p>
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
        num_pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=200, value=2, step=1)
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
                            if st.download_button(
                                label=f"📥 Télécharger {csv_filename}",
                                data=file,
                                file_name=csv_filename,
                                mime="text/csv",
                                key="download_csv",
                                on_click=lambda: st.balloons()  # Directement sur l'événement click
                            ):
                                pass  

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
                            <h3 style="margin: 0 0 5px 0; color: #1f2937;">{' '.join(nom.split()[1:])}</h3>
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

# Partie 13 : Dashboard Données Nettoyées
elif menu == "📊 Dashboard Données Nettoyées":
    
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #4f46e5;
            --secondary-color: #10b981;
            --accent-color: #f59e0b;
            --danger-color: #ef4444;
        }
        
        /* Thème général */
        .dashboard-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
            text-align: center;
            margin: 0.5rem 0 1.5rem 0;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Cartes */
        .plot-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--primary-color);
            transition: all 0.3s ease;
        }
        
        .plot-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }
        
        .plot-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .plot-icon {
            font-size: 1.5rem;
            margin-right: 0.75rem;
            color: var(--primary-color);
        }
        
        .plot-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #111827;
            margin: 0;
        }
        
        /* KPI Cards */
        .kpi-card {
            background: white;
            border-radius: 10px;
            padding: 1.25rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-top: 3px solid var(--primary-color);
            transition: all 0.2s;
        }
        
        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(79, 70, 229, 0.1);
        }
        
        .kpi-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #111827;
            margin: 0.25rem 0;
        }
        
        .kpi-label {
            font-size: 0.9rem;
            color: #6b7280;
            margin: 0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1rem;
            border-radius: 8px !important;
            background-color: #f9fafb !important;
            transition: all 0.2s;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color) !important;
            color: white !important;
        }
        
        /* Boutons */
        .stDownloadButton>button {
            background-color: var(--secondary-color) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            width: 100%;
            transition: all 0.2s;
        }
        
        .stDownloadButton>button:hover {
            background-color: #0d9b6c !important;
            transform: translateY(-1px);
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25em 0.6em;
            font-size: 75%;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 10px;
            background-color: #f3f4f6;
            color: #111827;
        }
    </style>
    """, unsafe_allow_html=True)

    # Dictionnaire des fichiers nettoyés
    fichiers_clean = {
        "👔 Vêtements Homme": "coinafrique-vetements-homme_clean.csv" ,
        "👟 Chaussures Homme": "coinafrique-chaussures-homme_clean.csv",
        "👕 Vêtements Enfants": "coinafrique-vetements-enfants_clean.csv",
        "👟 Chaussures Enfants": "coinafrique-chaussures-enfants_clean.csv"
    }

    # Configuration des catégories et des colonnes d'état
    category_config = {
        "👔 Vêtements Homme": {
            "type": "V1_type_habits",
            "features": {
                "Type": r'([A-Za-z]+)'
            }
        },
        "👟 Chaussures Homme": {
            "type": "V1_type_chaussures",
            "features": {
                "Type": r'([A-Za-z]+)'
            }
        },
        "👕 Vêtements Enfants": {
            "type": "V1_type_habits",
            "features": {
                "Type": r'([A-Za-z]+)'
            }
        },
        "👟 Chaussures Enfants": {
            "type": "V1_type_chaussures",
            "features": {
                "Type": r'([A-Za-z]+)'
            }
        },
    }

    # Création des onglets pour chaque catégorie et un onglet pour toutes les catégories
    tabs = st.tabs(["🌐 Toutes catégories"] + list(fichiers_clean.keys()))

    all_data = []
    loaded_data = {}

    # Chargement des données nettoyées pour chaque catégorie
    for category, filename in fichiers_clean.items():
        filepath = os.path.join("webscraper_data", filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Nettoyage du prix pour garantir le format numérique
            if 'V2_prix' in df.columns:
                df['V2_prix'] = (
                    df['V2_prix']
                    .astype(str)
                    .str.replace(r"[^\d]", "", regex=True)
                    .replace("", "0")
                    .astype(float)
                )
            df["Catégorie"] = category
            config = category_config[category]

            for feature_name, regex_pattern in config["features"].items():
                df[feature_name] = df[config["type"]].astype(str).str.extract(regex_pattern, flags=re.IGNORECASE)[0]
           
            loaded_data[category] = df
            all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

    # Affichage des KPI globaux et des graphiques dans le premier onglet
    with tabs[0]:
        if not combined_df.empty:
            # === KPI GLOBALS ===
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                <div class="kpi-card">
                    <p class="kpi-label">Annonces totales</p>
                    <p class="kpi-value">%s</p>
                    <i class="fas fa-list-ol" style="color: var(--primary-color);"></i>
                </div>
                """ % f"{len(combined_df):,}", unsafe_allow_html=True)
            
            with col2:
                prix_moyen = combined_df['V2_prix'].mean()
                valeur_a_afficher = f"{prix_moyen:,.0f} FCFA" if not pd.isna(prix_moyen) else "N/A"
                st.markdown(f"""
                <div class="kpi-card">
                    <p class="kpi-label">Prix moyen</p>
                    <p class="kpi-value">{valeur_a_afficher}</p>
                    <i class="fas fa-money-bill-wave" style="color: var(--secondary-color);"></i>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="kpi-card">
                    <p class="kpi-label">Catégories</p>
                    <p class="kpi-value">%d</p>
                    <i class="fas fa-tags" style="color: var(--danger-color);"></i>
                </div>
                """ % len(loaded_data), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="kpi-card">
                    <p class="kpi-label">Villes actives</p>
                    <p class="kpi-value">%d</p>
                    <i class="fas fa-map-marker-alt" style="color: var(--accent-color);"></i>
                </div>
                """ % combined_df['V3_adresse'].nunique(), unsafe_allow_html=True)

            # === GRAPHIQUES ===
            with st.container():
                st.markdown("""
                <div class="plot-card">
                    <div class="plot-header">
                        <div class="plot-icon">📊</div>
                        <h3 class="plot-title">Répartition par catégorie</h3>
                    </div>
                """, unsafe_allow_html=True)
                
            fig_cat_dist = px.pie(
                combined_df,
                names='Catégorie',
                title='',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.3,
                category_orders={"Catégorie": [
                    "Vêtements Homme",
                    "Chaussures Homme",
                    "Vêtements Enfants",
                    "Chaussures Enfants"
                ]}
            )
            fig_cat_dist.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",  # vertical
                    x=1.05,           # à droite du graphique
                    y=0.5,
                    xanchor="left",
                    yanchor="middle"
                )
            )
            st.plotly_chart(fig_cat_dist, use_container_width=True)

            with st.container():
                st.markdown("""
                <div class="plot-card">
                    <div class="plot-header">
                        <div class="plot-icon">💲</div>
                        <h3 class="plot-title">Comparaison des prix</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                fig_price_comp = px.box(
                combined_df, x='Catégorie', y='V2_prix',
                title='',
                color='Catégorie',
                labels={'V2_prix': 'Prix (FCFA)', 'Catégorie': ''},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
                fig_price_comp.update_layout(xaxis_title=None)
                st.plotly_chart(fig_price_comp, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with st.container():
                st.markdown("""
                <div class="plot-card">
                    <div class="plot-header">
                        <div class="plot-icon">🏙️</div>
                        <h3 class="plot-title">Top villes</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                top_cities = combined_df['V3_adresse'].value_counts().nlargest(10).reset_index()
                fig_top_cities = px.bar(
                    top_cities, x='V3_adresse', y='count',
                    labels={'count': "Nombre d'annonces"},
                    color='count',
                    color_continuous_scale="Viridis",
                    text='count'
                )
                fig_top_cities.update_traces(textposition='outside')
                fig_top_cities.update_layout(xaxis_title=None, yaxis_title=None)
                st.plotly_chart(fig_top_cities, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

 # Partie 14 : Affichage des données pour chaque catégorie dans des onglets séparés
    for i, (category, df) in enumerate(loaded_data.items(), start=1):
        with tabs[i]:
            config = category_config[category]
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem;">
                <span style="font-size: 1.8rem;">{category.split()[0]}</span>
                <h2 style="margin: 0; color: #111827;">Analyse des {category.split()[1]}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <p class="kpi-label">Annonces</p>
                    <p class="kpi-value">{len(df):,}</p>
                    <i class="fas fa-box-open" style="color: var(--primary-color);"></i>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                prix_moyen = df['V2_prix'].mean()
                valeur_a_afficher = f"{prix_moyen:,.0f} FCFA" if not pd.isna(prix_moyen) else "N/A"
                st.markdown(f"""
                <div class="kpi-card">
                    <p class="kpi-label">Prix moyen</p>
                    <p class="kpi-value">{valeur_a_afficher}</p>
                    <i class="fas fa-coins" style="color: var(--accent-color);"></i>
                </div>
                """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class="plot-card">
                    <div class="plot-header">
                        <div class="plot-icon">💰</div>
                        <h3 class="plot-title">Analyse des prix</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    # Histogramme des prix
                    fig_price_dist = px.histogram(
                        df, 
                        x='V2_prix',
                        nbins=20,
                        labels={'V2_prix': 'Prix (FCFA)'},
                        color_discrete_sequence=['#4f46e5'],
                        title='Distribution des prix'
                    )
                    fig_price_dist.update_layout(
                        xaxis=dict(
                            tickmode='array',
                            tickvals=[0, 100000, 200000, 300000, 400000],
                            ticktext=['0', '100k', '200k', '300k', '400k']
                        ),
                        height=400
                    )
                    st.plotly_chart(fig_price_dist, use_container_width=True)
                
                with col2:
                    # Boxplot des prix
                    fig_price_box = px.box(
                        df,
                        y='V2_prix',
                        labels={'V2_prix': 'Prix (FCFA)'},
                        color_discrete_sequence=['#10b981'],
                        title='Distribution statistique'
                    )
                    fig_price_box.update_layout(height=400)
                    st.plotly_chart(fig_price_box, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

            if any(feat in df.columns for feat in config["features"]):
                with st.container():
                    st.markdown("""
                    <div class="plot-card">
                        <div class="plot-header">
                            <div class="plot-icon">🔍</div>
                            <h3 class="plot-title">Caractéristiques des produits</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    features_to_show = [feat for feat in config["features"] if feat in df.columns]
                    tabs_features = st.tabs(features_to_show)
                    
                    for j, feature in enumerate(features_to_show):
                        with tabs_features[j]:
                            if df[feature].notna().sum() > 0:
                                col1, col2 = st.columns(2)
                                with col1:
                                    # Diagramme circulaire
                                    fig_pie = px.pie(
                                        df[feature].value_counts().reset_index(),
                                        values='count',
                                        names=feature,
                                        title=f'Répartition par {feature.lower()}',
                                        hole=0.4,
                                        color_discrete_sequence=px.colors.qualitative.Pastel
                                    )
                                    fig_pie.update_layout(height=400)
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                
                                with col2:
                                    # Diagramme à barres
                                    fig_bar = px.bar(
                                        df[feature].value_counts().reset_index(),
                                        x=feature,
                                        y='count',
                                        labels={'count': "Nombre d'annonces"},
                                        color='count',
                                        color_continuous_scale="Viridis",
                                        title=f'Nombre d\'annonces par {feature.lower()}',
                                        text='count'
                                    )
                                    fig_bar.update_traces(textposition='outside')
                                    fig_bar.update_layout(
                                        xaxis_title=None,
                                        yaxis_title=None,
                                        height=400
                                    )
                                    st.plotly_chart(fig_bar, use_container_width=True)
                            else:
                                st.warning(f"Aucune donnée disponible pour {feature}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

           
            if any(feat in df.columns for feat in config["features"]):
                with st.container():
                    st.markdown("""
                    <div class="plot-card">
                        <div class="plot-header">
                            <div class="plot-icon">📈</div>
                            <h3 class="plot-title">Relation prix/caractéristiques</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    feature = next((feat for feat in config["features"] if feat in df.columns), None)
                    if feature and df[feature].notna().sum() > 0:
                        fig_scatter = px.scatter(
                            df,
                            x=feature,
                            y='V2_prix',
                            color='etat' if 'etat' in df.columns else None,
                            labels={'V2_prix': 'Prix (FCFA)'},
                            title=f'Prix vs {feature}',
                            hover_data=[config["type"]]
                        )
                        fig_scatter.update_layout(height=500)
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.warning("Données insuffisantes pour cette analyse")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                 
          # Partie 15 : Affichage des données nettoyées dans un tableau          
                        # ...existing code...
            with st.expander(f"🔍 Données nettoyées - {' '.join(category.split()[1:])} (10 premières lignes)", expanded=False):
                colonnes_a_afficher = [
                    'V1_type_habits', 'V2_prix', 'V3_adresse', 'V4_image_lien-src',  
                ]
                df_filtre = df[[col for col in colonnes_a_afficher if col in df.columns]].head(10)
                st.dataframe(df_filtre, use_container_width=True, height=400)
            # ...existing code...

                PAGES_PAR_CATEGORIE = {
                    "👔 Vêtements Homme": 119,
                    "👟 Chaussures Homme": 199,
                    "👕 Vêtements Enfants": 22,
                    "👟 Chaussures Enfants": 8
                }

                csv = df_filtre.to_csv(index=False).encode('utf-8')

                if st.download_button(
                    label=f"📥 Télécharger les données nettoyées pour la categorie  {' '.join(category.split()[1:])}",
                    data=csv,
                    file_name=f"coinafrique_{'_'.join(category.split()[1:]).lower()}_clean.csv",
                    mime="text/csv",
                    key=f"dl_{category}"  
                ):
                    st.session_state['show_download_message'] = True  

                if st.session_state.get('show_download_message', False):
                    st.markdown(f"""
                    <div style="
                        background: #f0fdf4;
                        border-left: 4px solid #10b981;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        margin: 1rem 0;
                    ">
                        <h3 style="color: #10b981; margin-top: 0;">✅ Téléchargement réussi</h3>
                        <p>Données téléchargées :</p>
                        <ul>
                            <li><strong>Catégorie :</strong> {' '.join(category.split()[1:])}</li>
                            <li><strong>Annonces :</strong> {len(df_filtre)}</li>
                            <li><strong>Pages totales :</strong> {PAGES_PAR_CATEGORIE[category]}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.session_state['show_download_message'] = False


# Partie 17 : si le menu sélectionné est "📝 Formulaire d'évaluation"
elif menu == "📝 Formulaire d'évaluation":
    st.markdown("""
    <style>
        .form-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
            margin-top: 20px;
            border-left: 5px solid #4f46e5;
            transition: all 0.3s ease;
        }
        .form-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }
        .form-title {
            font-size: 28px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 10px;
            text-align: center;
            background: linear-gradient(90deg, #4f46e5, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .form-description {
            text-align: center;
            color: #6b7280;
            margin-bottom: 30px;
            font-size: 16px;
        }
        .form-section {
            margin-bottom: 25px;
        }
        .form-label {
            font-weight: 600;
            color: #374151;
            margin-bottom: 8px;
            display: block;
        }
        .required-field::after {
            content: " *";
            color: #ef4444;
        }
        .rating-container {
            display: flex;
            justify-content: space-between;
            margin-top: 5px;
        }
        .rating-label {
            font-size: 12px;
            color: #6b7280;
        }
        .stButton>button {
            width: 100%;
            padding: 12px;
            font-weight: 600;
            background-color: #4f46e5 !important;
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #4338ca !important;
            transform: translateY(-1px);
        }
        .success-message {
            text-align: center;
            padding: 15px;
            background-color: #f0fdf4;
            border-radius: 8px;
            border-left: 4px solid #10b981;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
 # Partie 18 : Affichage du formulaire d'évaluation
    st.markdown('<div class="form-description">Votre avis compte pour nous. Aidez-nous à améliorer cette application.</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("evaluation_form"):
            st.markdown("### Informations personnelles")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<span class="form-label required-field">Nom complet</span>', unsafe_allow_html=True)
                nom = st.text_input(
                    label="Nom complet",
                    placeholder="Ex: Niako Kebe",
                    help="Votre prénom et nom",
                    key="nom",
                    label_visibility="collapsed"
                )
            with col2:
                st.markdown('<span class="form-label required-field">Email</span>', unsafe_allow_html=True)
                email = st.text_input(
                    label="Email",
                    placeholder="votre@email.com",
                    help="Nous ne partagerons jamais votre email",
                    key="email",
                    label_visibility="collapsed"
                )
            st.markdown('<span class="form-label">Téléphone (optionnel)</span>', unsafe_allow_html=True)
            telephone = st.text_input(
                label="Téléphone",
                placeholder="+221 77 077 70 77",
                key="tel",
                label_visibility="collapsed"
            )

            st.markdown("### Évaluation")
            st.markdown('<span class="form-label required-field">Date d\'évaluation</span>', unsafe_allow_html=True)
            date_eval = st.date_input(
                label="Date d'évaluation",
                value=datetime.today(),
                key="date_eval",
                label_visibility="collapsed"
            )

            st.markdown('<span class="form-label required-field">Note globale</span>', unsafe_allow_html=True)
            note = st.slider(
                label="Note globale",
                min_value=1,
                max_value=10,
                value=9,
                key="note",
                label_visibility="collapsed"
            )

            st.markdown("""
            <div class="rating-container">
                <span class="rating-label">1 - Insatisfaisant</span>
                <span class="rating-label">10 - Excellent</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Commentaires")
            st.markdown('<span class="form-label">Vos retours (optionnel)</span>', unsafe_allow_html=True)
            commentaire = st.text_area(
                label="Vos retours",
                placeholder="Qu'avez-vous aimé ? Que pouvons-nous améliorer ?",
                height=120,
                key="comment",
                label_visibility="collapsed"
            )
            # Initialiser l'état s'il n'existe pas encore
            if "evaluation_submitted" not in st.session_state:
                st.session_state["evaluation_submitted"] = False

            # Bouton de soumission
            submitted = st.form_submit_button("Soumettre mon évaluation", type="primary")

            if submitted:
                if not nom or not email:
                    st.error("Veuillez remplir les champs obligatoires (marqués d'un *)")
                else:
                    feedback_data = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "nom_complet": nom,
                        "email": email,
                        "telephone": telephone if telephone else "Non renseigné",
                        "date_evaluation": date_eval.strftime("%Y-%m-%d"),
                        "note": note,
                        "commentaire": commentaire if commentaire else "Aucun commentaire"
                    }

                    file_path = "feedback.csv"
                    try:
                        if os.path.exists(file_path):
                            df_old = pd.read_csv(file_path)
                        else:
                            df_old = pd.DataFrame(columns=feedback_data.keys())

                        df_new = pd.concat([df_old, pd.DataFrame([feedback_data])], ignore_index=True)
                        df_new.to_csv(file_path, index=False)

                        st.session_state["evaluation_submitted"] = True

                    except Exception as e:
                        st.error(f"Une erreur est survenue : {str(e)}")

            if st.session_state.get("evaluation_submitted"):
                st.markdown("""
                <div class="success-message">
                    <h3 style="color: #10b981; margin-bottom: 10px;">✅ Merci pour votre évaluation !</h3>
                    <p>Vos retours ont été enregistrés avec succès.</p>
                </div>
                """, unsafe_allow_html=True)