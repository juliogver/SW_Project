import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target websites
sources = [
    "https://www.lemonde.fr/technologies/",
    "https://www.lequipe.fr/Rugby/",
    "https://www.reuters.com/technology/"
]

articles = []

# Function to scrape articles
def scrape_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for article in soup.find_all("article")[:5]:  # Limit to 5 per source
        title = article.find("h2").text if article.find("h2") else "No Title"
        link = article.find("a")["href"] if article.find("a") else "No Link"
        
        # Get article content
        if link.startswith("/"):
            link = f"https://www.lemonde.fr{link}"
        article_page = requests.get(link)
        article_soup = BeautifulSoup(article_page.text, "html.parser")
        content = " ".join([p.text for p in article_soup.find_all("p")])

        articles.append({
            "Article Link": link,
            "Article Title": title,
            "Article Content": content
        })

# Scrape each source
for source in sources:
    scrape_articles(source)

# Convert to DataFrame and save
df = pd.DataFrame(articles)
df.to_csv("../data/articles_scraped.csv", index=False, encoding="utf-8")

print("✅ Articles scraped and saved successfully!")




