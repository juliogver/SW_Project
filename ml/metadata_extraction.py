import os
import pandas as pd
import spacy
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from transformers import pipeline
from SPARQLWrapper import SPARQLWrapper, JSON

# Charger le modèle NLP de spaCy (français)
nlp = spacy.load("fr_core_news_md")

# Charger le classificateur de texte (Transformer pré-entraîné)
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

# Chargement du dataset
csv_path = "../data/articles.csv"
df = pd.read_csv(csv_path)

# Définition de l’espace de noms RDF
EX = Namespace("http://myproject.org/ai_ontology#")

# Création du graphe RDF
g = Graph()
g.parse("../data/rdf_data.ttl", format="turtle")

# Liste de domaines possibles pour classification
domains = ["Sport", "Intelligence Artificielle", "Technologie", "Éducation", "Trading"]

# Fonction pour extraire automatiquement des métadonnées d'un article
def extract_metadata(article):
    doc = nlp(article)
    entities = {ent.label_: ent.text for ent in doc.ents}

    metadata = {
        "topics": [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "EVENT"]],
        "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "people": [ent.text for ent in doc.ents if ent.label_ == "PER"],
        "locations": [ent.text for ent in doc.ents if ent.label_ == "LOC"]
    }
    return metadata

# Fonction pour enrichir l'article avec DBpedia
def query_dbpedia(entity):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = f"""
    SELECT ?abstract WHERE {{
        dbr:{entity.replace(" ", "_")} dbo:abstract ?abstract .
        FILTER (lang(?abstract) = "fr")
    }} LIMIT 1
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            return result["abstract"]["value"]
    except:
        return None

# Ajouter les métadonnées et enrichir le RDF
for _, row in df.iterrows():
    article_uri = URIRef(EX[f"Article_{row['ID']}"])
    extracted_metadata = extract_metadata(row["Article Content"])

    # Classification du domaine avec NLP
    classification = classifier(row["Article Content"], candidate_labels=domains)
    best_domain = classification["labels"][0]
    
    # Ajout du domaine automatique
    g.add((article_uri, EX.hasDomain, Literal(best_domain)))

    # Ajout des entités reconnues
    for topic in extracted_metadata["topics"]:
        topic_uri = URIRef(EX[f"Topic_{topic.replace(' ', '_')}"])
        g.add((article_uri, EX.hasTopic, topic_uri))

        # Enrichissement via DBpedia
        dbpedia_info = query_dbpedia(topic)
        if dbpedia_info:
            g.add((topic_uri, EX.hasDBpediaAbstract, Literal(dbpedia_info)))

    for person in extracted_metadata["people"]:
        person_uri = URIRef(EX[f"Person_{person.replace(' ', '_')}"])
        g.add((article_uri, EX.hasPerson, person_uri))

    for organization in extracted_metadata["organizations"]:
        org_uri = URIRef(EX[f"Organization_{organization.replace(' ', '_')}"])
        g.add((article_uri, EX.hasOrganization, org_uri))

    for location in extracted_metadata["locations"]:
        loc_uri = URIRef(EX[f"Location_{location.replace(' ', '_')}"])
        g.add((article_uri, EX.hasLocation, loc_uri))

# Sauvegarde du graphe RDF mis à jour
g.serialize("../data/rdf_data.ttl", format="turtle")

print("✅ Métadonnées extraites et RDF mis à jour avec succès !")
