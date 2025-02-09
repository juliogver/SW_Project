from flask import Flask, render_template, request
from rdflib import Graph

app = Flask(__name__)

# Load the RDF graph
g = Graph()
g.parse("../data/rdf_data_llm.ttl", format="turtle")

# Load SPARQL queries from sparql_queries.rq
def load_queries(file_path):
    queries = {}
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        # Split queries by double newline
        query_blocks = content.split("\n\n")
        for block in query_blocks:
            lines = block.strip().split("\n")
            # Extract query name from the first line (comment)
            query_name = lines[0].replace("#", "").strip()
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
    sparql_result = g.query(sparql_query)

    # Convert SPARQLResult into a list of dictionaries with cleaned URIs
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
