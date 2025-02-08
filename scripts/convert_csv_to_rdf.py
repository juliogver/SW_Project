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
    
    g.add((article_uri, EX.hasTitle, Literal(row["Article Title"])))
    g.add((article_uri, EX.hasAuthor, Literal(row["Article Author Name"])))
    g.add((article_uri, EX.hasDate, Literal(row["Article Date"])))
    g.add((article_uri, EX.hasContent, Literal(row["Article Content"])))

# Sauvegarde du graphe RDF
g.serialize("../data/rdf_data.ttl", format="turtle")

print("✅ Le fichier data.rdf a été généré avec succès !")
