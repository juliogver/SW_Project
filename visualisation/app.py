from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return "Bienvenue sur l’interface de visualisation RDF"

if __name__ == "__main__":
    app.run(debug=True)
