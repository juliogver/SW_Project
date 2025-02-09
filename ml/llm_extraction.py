import os
import pandas as pd
import openai
from rdflib import Graph, Namespace, URIRef, Literal
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

import json  # Ajoutez cette ligne pour parser le JSON

load_dotenv("../key.env")  # Charger le fichier spécifique

# OpenAI API key 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# RDF Namespace
EX = Namespace("http://myproject.org/ai_ontology#")

# Load the dataset
csv_path = "../data/articles.csv"
df = pd.read_csv(csv_path)

# Load existing RDF graph
g = Graph()
g.parse("../data/rdf_data.ttl", format="turtle")

# Function to extract metadata using GPT
def extract_metadata_llm(content):
    prompt = f"""
    Extract structured metadata from the following article:
    ---
    {content}
    ---
    Provide JSON output with fields:
    - topics: List of key topics
    - organizations: List of organizations mentioned
    - people: List of individuals mentioned
    - locations: List of geographical locations mentioned
    Output should be a valid JSON format without any extra text.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o", 
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )

    # 🔹 Nettoyer les backticks de la réponse
    raw_response = response["choices"][0]["message"]["content"].strip()
    
    if raw_response.startswith("```json"):
        raw_response = raw_response.replace("```json", "").replace("```", "").strip()

    # 🔹 Convertir la réponse en JSON
    try:
        metadata = json.loads(raw_response)
    except json.JSONDecodeError:
        print("Erreur : Impossible de parser la réponse LLM en JSON.")
        print("Réponse reçue :", raw_response)  # Debugging
        return None  # Retourne `None` si la réponse n'est pas un JSON valide
    
    return metadata

# Function to enrich the article with DBpedia
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

# Process each article and extract metadata
for _, row in df.iterrows():
    article_uri = URIRef(EX[f"Article_{row['ID']}"])
    
    # Extract metadata using LLM
    metadata = extract_metadata_llm(row["Article Content"])

    for topic in metadata["topics"]:
        topic_uri = URIRef(EX[f"Topic_{topic.replace(' ', '_')}"])
        g.add((article_uri, EX.hasTopic, topic_uri))
        
        # Enrich with DBpedia
        dbpedia_info = query_dbpedia(topic)
        if dbpedia_info:
            g.add((topic_uri, EX.hasDBpediaAbstract, Literal(dbpedia_info)))

    for person in metadata["people"]:
        person_uri = URIRef(EX[f"Person_{person.replace(' ', '_')}"])
        g.add((article_uri, EX.hasPerson, person_uri))

    for organization in metadata["organizations"]:
        org_uri = URIRef(EX[f"Organization_{organization.replace(' ', '_')}"])
        g.add((article_uri, EX.hasOrganization, org_uri))

    for location in metadata["locations"]:
        loc_uri = URIRef(EX[f"Location_{location.replace(' ', '_')}"])
        g.add((article_uri, EX.hasLocation, loc_uri))

# Save updated RDF graph
g.serialize("../data/rdf_data.ttl", format="turtle")

print("Metadata extracted using LLM and RDF updated successfully!")
