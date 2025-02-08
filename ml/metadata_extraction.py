from transformers import pipeline

nlp = pipeline("ner")
text = "This is an article written by John Doe about AI."

entities = nlp(text)
print(entities)  # Affiche les métadonnées extraites
