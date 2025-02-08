import pandas as pd
import os

# Définition des articles (données fictives, à remplacer par un scraping ou API)
articles = [
    {
        "ID": 1,
        "Article Link": "https://www.livefoot.fr/france/ligue1/psg.php",
        "Article Title": "Introduction à l'Intelligence Artificielle",
        "Article Date": "2024-02-01",
        "Article Author Name": "John Doe",
        "Article Topics": "IA, Machine Learning",
        "Article Main Domain": "Artificial Intelligence",
        "Article Source": "Tech Magazine",
        "Article Content": "L'intelligence artificielle révolutionne de nombreux secteurs..."
    }
    
]

# Création du DataFrame
df = pd.DataFrame(articles)

# Enregistrer dans un sous-dossier du projet (ex: ./data/)
output_dir = "../data/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_path = os.path.join(output_dir, "articles.csv")

df.to_csv(csv_path, index=False, encoding="utf-8")

print(f"✅ Le fichier dataset.csv a été généré avec succès dans : {csv_path}")
