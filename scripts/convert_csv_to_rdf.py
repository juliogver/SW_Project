import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal

# Charger le dataset CSV
df = pd.read_csv("../data/articles.csv")

# Création du graphe RDF
g = Graph()

# Définition de l’espace de noms
EX = Namespace("http://myproject.org/ai_ontology#")

# Ajouter des articles au graphe
for _, row in df.iterrows():
    article_uri = URIRef(EX[f"Article_{row['ID']}"])
    author_uri = URIRef(EX[f"Author_{row['Article Author Name'].replace(' ', '_')}"])  
    domain_uri = Literal(row["Article Main Domain"])
    
    # Ajout des propriétés de base
    g.add((article_uri, EX.hasTitle, Literal(row["Article Title"])))
    g.add((article_uri, EX.hasAuthor, author_uri)) 
    g.add((article_uri, EX.hasDate, Literal(row["Article Date"])))
    g.add((article_uri, EX.hasContent, Literal(row["Article Content"])))
    g.add((article_uri, EX.hasDomain, domain_uri))

    # Ajout de la relation entre l'auteur et l'article
    g.add((author_uri, EX.wroteArticle, article_uri))

    # Ajout des sujets (topics)
    topics = row["Article Topics"].split(", ")  
    for topic in topics:
        topic_uri = URIRef(EX[f"Topic_{topic.replace(' ', '_')}"])  
        g.add((article_uri, EX.hasTopic, topic_uri))

# Sauvegarde du graphe RDF
g.serialize("../data/rdf_data.ttl", format="turtle")

print("Le fichier rdf_data.ttl a été généré avec succès !")
