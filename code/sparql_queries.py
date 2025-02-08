from rdflib import Graph

# Charger le graphe RDF
g = Graph()
g.parse("data.rdf", format="turtle")

# Définition de la requête SPARQL
query = """
PREFIX ex: <http://example.org/articles#>

SELECT ?article ?title ?author WHERE {
  ?article ex:hasTitle ?title .
  ?article ex:hasAuthor ?author .
}
"""

# Exécution de la requête
results = g.query(query)

# Affichage des résultats
print("\n🔍 Résultats de la requête SPARQL :")
for row in results:
    print(f"📄 Article: {row.title}, Auteur: {row.author}")
