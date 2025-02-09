# SW_Project

## Prérequis
Avant d'exécuter le projet, assurez-vous d'avoir installé les packages et dépendances suivantes.

### 1. Installation des extensions
Les extensions suivantes sont nécessaires pour le bon fonctionnement du projet :
- **jena-extension**
- **Turtle Language Server**

Assurez-vous qu'elles sont installées dans votre environnement de développement.

### 2. Installation des dépendances Python
Dans le terminal, exécutez la commande suivante pour installer toutes les dépendances nécessaires listées dans `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 3. Installation du package pour le Machine Learning
Pour utiliser les fonctionnalités de traitement du langage naturel (NLP), téléchargez le modèle **fr_core_news_md** de spaCy en exécutant la commande suivante :

```bash
python -m spacy download fr_core_news_md
```

## Description du Modèle NLP
Le modèle **fr_core_news_md** de spaCy est un outil performant de traitement automatique du langage naturel (NLP) pour le français. Il permet notamment de :
- Segmenter le texte en phrases.
- Identifier les relations grammaticales.
- Extraire automatiquement des entités nommées telles que :
  - **PER** : Personnes.
  - **ORG** : Organisations.
  - **LOC** : Lieux.
  - **PRODUCT, EVENT** : Produits et événements.

## Exécution du Projet
Une fois toutes les dépendances installées, vous pouvez exécuter le projet avec ces étapes:

```bash
cd .\scripts\ 
```
```bash
python .\csv_generator.py
python .\csv_generator.py
python .\web_scrapping.py
python .\convert_csv_to_rdf.py
```
```bash
cd ..\ml\   
```
```bash
python .\metadata_extraction.py
python .\llm_extraction.py     
```
```bash
cd ..\app\    
```
```bash
python .\reporting.py    
```

Assurez-vous que votre environnement Python est correctement configuré et que toutes les installations sont bien effectuées.

