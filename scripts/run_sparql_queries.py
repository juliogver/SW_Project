from rdflib import Graph

# Charger le fichier RDF
g = Graph()
g.parse("../data/rdf_data.ttl", format="turtle")

# Quand on veut utiliser le ml 
# g.parse("../data/rdf_data_ml.ttl", format="turtle")

# Charger et nettoyer les requêtes SPARQL
with open("sparql_queries.rq", "r", encoding="utf-8") as f:
    queries = [q.strip() for q in f.read().split("\n\n") if q.strip()]  # Suppression des requêtes vides

# Fonction pour enlever les commentaires SPARQL
def clean_query(query):
    lines = query.split("\n")
    clean_lines = [line for line in lines if not line.strip().startswith("#")]
    return "\n".join(clean_lines).strip()

# Exécuter chaque requête et afficher les résultats
for i, query in enumerate(queries, 1):
    cleaned_query = clean_query(query)
    
    print(f"\n🔹 Exécution de la requête {i}:")
    print(cleaned_query)

    try:
        results = g.query(cleaned_query)
        
        # Afficher correctement les résultats
        for row in results:
            formatted_row = tuple(
                str(value).split("#")[-1] if isinstance(value, str) and "#" in str(value) else str(value)
                for value in row
            )
            print(formatted_row)
            
    except Exception as e:
        print(f"Erreur dans la requête {i}: {e}")
