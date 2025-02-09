from flask import Flask, render_template, request
from rdflib import Graph

app = Flask(__name__)

# Load the RDF graph
g = Graph()
g.parse("../data/rdf_data.ttl", format="turtle")

# Load SPARQL queries from sparql_queries.rq
def load_queries(file_path):
    queries = {}
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        query_blocks = content.split("\n\n")  # Split queries by double newline
        for block in query_blocks:
            lines = block.strip().split("\n")
            query_name = lines[0].replace("#", "").strip()  # Extract query name from comment
            query_body = "\n".join(lines[1:]).strip()
            queries[query_name] = query_body
    return queries

# Load queries from the file
queries = load_queries("../scripts/sparql_queries.rq")

@app.route("/")
def index():
    return render_template("index.html", queries=queries.keys())

@app.route("/query", methods=["POST"])
def query():
    query_name = request.form["query"]
    sparql_query = queries[query_name]

    if sparql_query.strip().upper().startswith("CONSTRUCT"):
        # Execute the CONSTRUCT query and add results to the main graph
        result_graph = g.query(sparql_query)
        new_triples = []

        for triple in result_graph:
            g.add(triple)  # Add the triple to the main graph
            new_triples.append(triple)

        # Log added triples (debugging purpose)
        print("Triples added to the graph:")
        for triple in new_triples:
            print(triple)

        # Optionally save to the TTL file 
        g.serialize(destination="../data/rdf_data.ttl", format="turtle")

        # Query newly added triples for confirmation
        confirmation_query = """
        PREFIX ai: <http://myproject.org/ai_ontology#>
        SELECT ?subject ?predicate ?object WHERE {
          ?subject ai:isHotTopic "true" .
        }
        """
        sparql_result = g.query(confirmation_query)

        results = [
            {
                "subject": str(row.subject).split("#")[-1],
                "predicate": str(row.predicate).split("#")[-1],
                "object": row.object
            }
            for row in sparql_result
        ]

        return render_template("results_construct.html", query=query_name, results=results)

    else:
        # For SELECT queries
        sparql_result = g.query(sparql_query)
        results = [
            {
                str(var): str(row[var]).split("#")[-1] if "#" in str(row[var]) else str(row[var])
                for var in sparql_result.vars
            }
            for row in sparql_result
        ]

        return render_template("results.html", query=query_name, results=results)

if __name__ == "__main__":
    app.run(debug=True)
