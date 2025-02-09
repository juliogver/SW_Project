import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime, timedelta

# 📌 Chemins des fichiers CSV
DATA_DIR = "../data/"
ARTICLES_CSV = os.path.join(DATA_DIR, "articles.csv")

# 📌 Liste des sources GRATUITES par thème
sources = {
    "Technologie": {
        "Numerama": "https://www.numerama.com/",
        "Clubic": "https://www.clubic.com/"
    },
    "Intelligence Artificielle": {
        "ActuIA": "https://www.actuia.com/",
        "Le Big Data": "https://www.lebigdata.fr/"
    },
    "Éducation": {
        "UNESCO": "https://www.unesco.org/fr/education",
        "Éduscol": "https://eduscol.education.fr/"
    },
    "Sport": {
        "Sports.fr": "https://www.sports.fr/",
        "Foot Mercato": "https://www.footmercato.net/"
    },
    "Trading": {
        "ZoneBourse": "https://www.zonebourse.com/",
        "Boursorama": "https://www.boursorama.com/"
    }
}

# 📌 Liste d'auteurs fictifs pour remplacer "Auteur Inconnu"
fake_authors = [
    "Jean Dupont", "Alice Martin", "Luc Lefebvre", "Sophie Bernard", "Éric Moreau",
    "Isabelle Fontaine", "Pierre Lambert", "Camille Durand", "Antoine Girard", "Julie Rousseau"
]

# 📌 Générer une date aléatoire entre "2024-01-01" et "2025-02-09"
def generate_random_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 9)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

# 📌 Charger les articles existants pour éviter les doublons et gérer les ID
if os.path.exists(ARTICLES_CSV):
    df_existing = pd.read_csv(ARTICLES_CSV)
    existing_ids = set(df_existing["ID"])
    next_id = max(existing_ids) + 1
else:
    df_existing = pd.DataFrame()
    existing_ids = set()
    next_id = 1  # Commencer les IDs à 1 s'il n'y a pas de fichier existant

# 📌 Fonction pour scraper un article
def scrape_article(source_name, url, category):
    global next_id  # Utilisation de la variable globale pour incrémenter l'ID

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction du titre
        title = soup.find("h1") or soup.find("title")
        title = title.text.strip() if title else "Titre non trouvé"

        # Extraction de la date (format ISO : YYYY-MM-DD)
        date = soup.find("time")
        date = date["datetime"][:10] if date and "datetime" in date.attrs else generate_random_date()

        # Extraction de l'auteur
        author = soup.find(class_="author") or soup.find("span", class_="byline")
        author = author.text.strip() if author else random.choice(fake_authors)  # Remplace "Inconnu"

        # Extraction du contenu (500 premiers caractères)
        content = soup.find("article") or soup.find("p")
        content = content.text.strip()[:500] if content else "Contenu non trouvé"

        # Créer un dictionnaire d'article
        article = {
            "ID": next_id,
            "Article Link": url,
            "Article Title": title,
            "Article Date": date,  # Format ISO (YYYY-MM-DD)
            "Article Author Name": author,
            "Article Topics": category,
            "Article Main Domain": category,
            "Article Source": source_name,  # Nom propre de la source
            "Article Content": content
        }

        next_id += 1  # Incrémentation pour le prochain article

        return article

    except Exception as e:
        print(f"⚠️ Erreur lors du scraping {url}: {e}")
        return None

# 📌 Récupération des articles scrappés
articles_list = []

for category, source_data in sources.items():
    for source_name, url in source_data.items():
        print(f"🔍 Scraping {category} depuis {source_name}...")
        article = scrape_article(source_name, url, category)
        if article:
            articles_list.append(article)
        time.sleep(random.uniform(2, 5))  # Pause pour éviter d'être bloqué

# 📌 Convertir en DataFrame et fusionner avec `articles.csv`
df_scraped = pd.DataFrame(articles_list)

if not df_scraped.empty:
    df_final = pd.concat([df_existing, df_scraped], ignore_index=True)
    df_final.to_csv(ARTICLES_CSV, index=False, encoding="utf-8")
    print(f"✅ {len(df_scraped)} nouveaux articles ajoutés à {ARTICLES_CSV} !")
else:
    print("⚠️ Aucun nouvel article n'a été ajouté.")

