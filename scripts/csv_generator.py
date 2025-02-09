import pandas as pd
import os

# Définition des articles (données fictives, à remplacer par un scraping ou API)
articles = [
    # Articles Sport
    {
        "ID": 1,
        "Article Link": "https://www.lequipe.fr/Rugby/Article/Avec-matthieu-jalibert-en-ouvreur-les-bleus-veulent-enfoncer-l-angleterre-dans-ses-doutes-samedi-a-twickenham/1538377",
        "Article Title": "L'équipe de France veut enfoncer l'Angleterre dans ses doutes",
        "Article Date": "2025-02-07",
        "Article Author Name": "Renaud Bourel",
        "Article Topics": "Rugby, France, Angleterre",
        "Article Main Domain": "Sport",
        "Article Source": "l'Équipe",
        "Article Content": "Emmenée par Matthieu Jalibert, titulaire de circonstance, l'équipe de France va tenter la passe de quatre face à des Anglais dans le doute mais déterminés à laver l'humiliation de 2023 (10-53). Une semaine après la rouste infligée aux malheureux Gallois, le Tournoi des 6 Nations va réellement commencer ce samedi à Twickenham (17 h 45)."
    },
    {
        "ID": 2,
        "Article Link": "https://www.lemonde.fr/sport/article/2025/02/08/comment-le-pactole-de-la-ligue-des-champions-amplifie-encore-les-inegalites-entre-les-clubs-de-ligue-1_6537109_3242.html",
        "Article Title": "Comment le pactole de la Ligue des champions amplifie encore les inégalités entre les clubs de Ligue 1",
        "Article Date": "2025-02-08",
        "Article Author Name": "Alexandre Lemarié",
        "Article Topics": "Football, Ligue des champions, Ligue 1",
        "Article Main Domain": "Sport",
        "Article Source": "Le Monde",
        "Article Content": "Une compétition européenne qui rapporte encore un peu plus à des « gros » clubs, souvent déjà en bonne santé, et une compétition nationale avec des « petits » en difficulté, qui se partagent les miettes. Plus que jamais, la Ligue 1 (L1), le championnat de France de football de première division, avance à « plusieurs vitesses », comme le soulignait un rapport sénatorial, à la fin d’octobre 2024.Cette saison, avec la nouvelle formule de la Ligue des champions (LDC), les revenus prévus par la fédération européenne (UEFA) pour les trente-six participants ont nettement augmenté. En effet, le pactole global à se partager s’élève à 2,467 milliards d’euros, ce qui représente une hausse de 400 millions d’euros par rapport à la période 2021-2024. Les quatre équipes françaises engagées – le Paris Saint-Germain (PSG), Monaco, Lille et Brest –, qui se sont toutes qualifiées pour la suite du tournoi, vont profiter de cette manne.Le club nordiste, qui a connu le meilleur parcours des formations tricolores – il occupe la 7e place à l’issue de la phase de Ligue, ce qui lui permet d’accéder directement aux huitièmes de finale –, est déjà assuré de toucher le jackpot. Selon les règles de distribution de l’UEFA, qui prévoit de multiples primes liées à la participation (18,62 millions d’euros), aux résultats (2,1 millions pour une victoire) ou au classement, le LOSC empochera au moins 51 millions d’euros. Sans compter les recettes afférentes aux droits télévisés, également distribuées par l’instance européenne, et celles de la billetterie. Au total, les Lillois devraient percevoir plus de 75 millions, d’après les estimations de L’Equipe."
    },
    {
        "ID": 3,
        "Article Link": "https://www.sports.fr/football/angleterre/manchester-city-se-prend-un-but-de-dingue-contre-une-d3-video-900943.html",
        "Article Title": "Manchester City se prend un but de dingue contre une D3 (vidéo)",
        "Article Date": "2025-02-08",
        "Article Author Name": "Arnold Fortin",
        "Article Topics": "Football, Manchester City, Angleterre",
        "Article Main Domain": "Sport",
        "Article Source": "Sports.fr",
        "Article Content": "Il n’y a décidément plus de match facile pour Manchester City. En grande difficulté depuis le mois d’octobre, et ce quelle que soit la compétition, l’équipe de Pep Guardiola a encore prouvé sa fragilité ce samedi en FA Cup. Pourtant opposés à Leyton Orient, pensionnaire de League One, les Citizens se sont retrouvés menés au score après un but fou.Voyant le portier mancunien avancé, Jamie Donley a tenté sa chance de près de quarante mètres et son ballon en cloche est allé taper la barre avant de rebondir dans le dos du malheureux Stefan Ortega, buteur contre son camp. De quoi donner l’avantage aux locaux dès la seizième minute de jeu dans un stade en délire.Les Skyblues ont ensuite rejoint les vestiaires avec ce petit but de retard malgré un possession de balle en leur faveur de 73% sur cette première période. Si l’équipe alignée par Pep Guardiola était largement remaniée et principalement composée de jeunes et d’habituels remplaçants, ce fait de jeu fait à nouveau tâche."
    },
    {
        "ID": 4,
        "Article Link": "https://www.footmercato.net/a4163736138665628157-leurope-sincline-face-au-psg-le-derby-madrilene-retourne-toute-lespagne",
        "Article Title": "L’Europe s’incline face au PSG, le derby madrilène retourne toute l’Espagne",
        "Article Date": "2025-02-07",
        "Article Author Name": "vdevillaire",
        "Article Topics": "Football, PSG, Real de Madrid",
        "Article Main Domain": "Sport",
        "Article Source": "Footmercato",
        "Article Content": "Le PSG assoit sa domination et impressionne les observateurs, le derby de Madrid électrise l’Espagne, le Real Madrid traverse une crise interne avec ses cadres, retrouvez dans votre revue de presse Foot Mercato les dernières informations de la presse sportive européenne."
    },
    {
        "ID": 5,
        "Article Link": "https://www.lemonde.fr/sciences/article/2024/10/08/le-nobel-de-physique-celebre-les-pionniers-de-l-intelligence-artificielle_6346731_1650684.html",
        "Article Title": "Le Nobel de physique célèbre les pionniers de l'intelligence artificielle",
        "Article Date": "2024-10-08",
        "Article Author Name": "David Larousserie",
        "Article Topics": "IA, Physique, Réseaux de neurones",
        "Article Main Domain": "Intelligence Artificielle",
        "Article Source": "Le Monde",
        "Article Content": "Le Prix Nobel de physique 2024 a été décerné à John Hopfield et Geoffrey Hinton pour leurs travaux pionniers sur les réseaux de neurones artificiels, fondamentaux pour l'apprentissage automatique."
    },
    {
        "ID": 6,
        "Article Link": "https://www.lemonde.fr/economie/article/2024/10/09/openai-va-ouvrir-un-bureau-a-paris_6347114_3234.html",
        "Article Title": "OpenAI va ouvrir un bureau à Paris",
        "Article Date": "2024-10-09",
        "Article Author Name": "Alexandre Piquard",
        "Article Topics": "IA, OpenAI, France",
        "Article Main Domain": "Intelligence Artificielle",
        "Article Source": "Le Monde",
        "Article Content": "OpenAI annonce l'ouverture d'un bureau à Paris d'ici fin 2024, renforçant sa présence en Europe continentale et soulignant l'importance de la France en matière d'innovation technologique."
    },
    {
        "ID": 7,
        "Article Link": "https://www.lemonde.fr/economie/article/2024/08/31/l-intelligence-artificielle-est-une-bulle-il-y-a-un-decalage-entre-les-couts-tres-importants-et-les-revenus-potentiels_6300034_3234.html",
        "Article Title": "« L'intelligence artificielle est une bulle : il y a un décalage entre les coûts, très importants, et les revenus potentiels »",
        "Article Date": "2024-08-31",
        "Article Author Name": "Alexandre Piquard",
        "Article Topics": "IA, Économie, Technologie",
        "Article Main Domain": "Intelligence Artificielle",
        "Article Source": "Le Monde",
        "Article Content": "Cory Doctorow critique la bulle de l'IA, signalant un déséquilibre entre les coûts élevés des technologies et les revenus potentiels, comparant ce phénomène à celui des débuts d'Internet."
    },
    {
        "ID": 8,
        "Article Link": "https://www.lemonde.fr/pixels/article/2024/08/06/comment-l-ia-bouscule-le-milieu-de-la-sante-mentale-plutot-que-de-payer-une-nouvelle-seance-chez-le-psy-j-allais-sur-chatgpt_6270640_4408996.html",
        "Article Title": "Comment l'IA bouscule le milieu de la santé mentale : « Plutôt que de payer une nouvelle séance chez le psy, j'allais sur ChatGPT »",
        "Article Date": "2024-08-06",
        "Article Author Name": "Hélène Pagesy",
        "Article Topics": "IA, Santé mentale, ChatGPT",
        "Article Main Domain": "Intelligence Artificielle",
        "Article Source": "Le Monde",
        "Article Content": "Les outils d'IA, comme les chatbots, révolutionnent le domaine de la santé mentale, offrant des alternatives accessibles aux thérapies traditionnelles, mais posant également des risques et des questions éthiques."
    },

    {
        "ID": 9,
        "Article Link": "https://www.ac-paris.fr/l-intelligence-artificielle-dans-l-education-130992",
        "Article Title": "L'intelligence artificielle dans l'éducation",
        "Article Date": "2024-09-15",
        "Article Author Name": "Christian-Jacques Cubells",
        "Article Topics": "IA, Éducation, Personnalisation des apprentissages",
        "Article Main Domain": "Éducation",
        "Article Source": "Académie de Paris",
        "Article Content": "L'IA permet de personnaliser les apprentissages en adaptant les activités aux besoins des élèves et en offrant un soutien individualisé. Elle sert également d'assistant pédagogique pour les enseignants, facilitant le suivi des progrès des élèves."
    },

    {
        "ID": 10,
        "Article Link": "https://www.unesco.org/fr/digital-education/artificial-intelligence",
        "Article Title": "L'intelligence artificielle dans l'éducation",
        "Article Date": "2024-10-10",
        "Article Author Name": "Miao Fengchun",
        "Article Topics": "IA, Éducation, Inclusion",
        "Article Main Domain": "Éducation",
        "Article Source": "UNESCO",
        "Article Content": "L'IA offre des opportunités pour relever les défis majeurs de l'éducation, innover dans les pratiques d'enseignement et d'apprentissage, tout en veillant à l'inclusion et à l'équité."
    },


    {
        "ID": 11,
        "Article Link": "https://www.igensia-education.fr/actualites/impact-intelligence-artificielle-education",
        "Article Title": "Rôle et impact de l'intelligence artificielle en éducation",
        "Article Date": "2024-08-20",
        "Article Author Name": "Anne-Sophie Van Eslande",
        "Article Topics": "IA, Éducation, Personnalisation",
        "Article Main Domain": "Éducation",
        "Article Source": "Igensia Education",
        "Article Content": "L'IA permet de personnaliser les apprentissages selon les besoins et les capacités d'assimilation de chacun, en proposant des exercices adaptés au niveau de chaque élève."
    },

    {
        "ID": 12,
        "Article Link": "https://www.lefigaro.fr/actualite-france/apprentissage-de-la-lecture-a-l-ecole-un-rapport-parlementaire-tire-la-sonnette-d-alarme-20240124",
        "Article Title": "Apprentissage de la lecture à l'école : un rapport parlementaire tire la sonnette d'alarme",
        "Article Date": "2024-01-24",
        "Article Author Name": "Caroline Beyer",
        "Article Topics": "Éducation, Lecture, Rapport parlementaire",
        "Article Main Domain": "Éducation",
        "Article Source": "Le Figaro",
        "Article Content": "Selon l'enquête internationale Pirls 2021, seuls 16 pour cent des enseignants français mettent en place des mesures de différenciation pédagogique, soulignant un besoin d'adaptation des méthodes d'enseignement."
    },

    {
        "ID": 13,
        "Article Link": "https://www.futura-sciences.com/tech/actualites/voiture-94-vols-voitures-sont-realises-effraction-voici-pourquoi-votre-vehicule-est-cible-facile-104567/",
        "Article Title": "94 % des vols de voitures sont réalisés sans effraction : voici pourquoi votre véhicule est une cible facile",
        "Article Date": "2025-01-15",
        "Article Author Name": "Flora Borsi",
        "Article Topics": "Technologie, Automobile, Sécurité",
        "Article Main Domain": "Technologie",
        "Article Source": "Futura Sciences",
        "Article Content": "Une étude récente révèle que 94 % des vols de voitures sont effectués sans effraction, principalement en raison de la vulnérabilité des systèmes d'entrée sans clé. Les voleurs utilisent des dispositifs pour intercepter le signal de la clé et déverrouiller le véhicule."
    },
    {
        "ID": 14,
        "Article Link": "https://www.un.org/fr/un75/impact-digital-technologies",
        "Article Title": "L'impact des technologies numériques",
        "Article Date": "2024-12-10",
        "Article Author Name": "Marjorie Cessac",
        "Article Topics": "Technologie, Numérique, Société",
        "Article Main Domain": "Technologie",
        "Article Source": "Nations Unies",
        "Article Content": "Les technologies numériques transforment les sociétés en améliorant la connectivité, l'inclusion financière et l'accès aux services. Elles présentent également des défis en matière de confidentialité, de sécurité et d'inégalités."
    },
    {
        "ID": 15,
        "Article Link": "https://www.lemonde.fr/sciences/article/2024/10/28/du-soin-a-la-surveillance-du-cerveau-sept-defis-pour-les-neurotechnologies_6363498_1650684.html",
        "Article Title": "Du soin à la surveillance du cerveau : sept défis pour les neurotechnologies",
        "Article Date": "2024-10-28",
        "Article Author Name": "Laure Belot",
        "Article Topics": "Technologie, Neurotechnologies, Santé",
        "Article Main Domain": "Technologie",
        "Article Source": "Le Monde",
        "Article Content": "Les neurotechnologies, telles que les implants cérébraux et les casques EEG, offrent des avancées médicales pour traiter des maladies résistantes aux traitements, mais posent des défis éthiques et de confidentialité."
    },
    {
        "ID": 16,
        "Article Link": "https://www.lemonde.fr/economie/article/2024/10/27/la-ruee-vers-l-energie-solaire-grande-gagnante-de-la-bataille-de-la-competitivite_6360750_3234.html",
        "Article Title": "La ruée vers l'énergie solaire, grande gagnante de la bataille de la compétitivité",
        "Article Date": "2024-10-27",
        "Article Author Name": "Alexandre Piquard",
        "Article Topics": "Technologie, Énergie solaire, Économie",
        "Article Main Domain": "Technologie",
        "Article Source": "Le Monde",
        "Article Content": "L'énergie solaire connaît une croissance rapide, avec une augmentation de 29 % de la capacité mondiale installée en 2024. Des pays traditionnellement dépendants des énergies fossiles investissent massivement dans des projets solaires."
    },
    {
        "ID": 17,
        "Article Link": "https://www.lefigaro.fr/international/presidentielle-americaine-un-trader-francais-mise-28-millions-de-dollars-sur-la-victoire-de-donald-trump-20241028",
        "Article Title": "Présidentielle américaine : un trader français mise 28 millions de dollars sur la victoire de Donald Trump",
        "Article Date": "2024-10-28",
        "Article Author Name": "JS",
        "Article Topics": "Trading, Élections américaines, Paris financiers",
        "Article Main Domain": "Trading",
        "Article Source": "Le Figaro",
        "Article Content": "Un trader français a parié 28 millions de dollars sur la réélection de Donald Trump lors de la présidentielle américaine de 2024, illustrant l'implication des traders dans les événements politiques majeurs."
    },
    {
        "ID": 18,
        "Article Link": "https://www.cafedelabourse.com/archive/article/10-conseils-pour-etre-un-meilleur-trader",
        "Article Title": "10 conseils pour être un meilleur trader",
        "Article Date": "2025-01-20",
        "Article Author Name": "Clémence Tanguy",
        "Article Topics": "Trading, Conseils, Stratégies",
        "Article Main Domain": "Trading",
        "Article Source": "Café de la Bourse",
        "Article Content": "Cet article propose dix conseils essentiels pour améliorer ses compétences en trading, notamment le choix du courtier, l'élaboration d'un plan de trading et l'utilisation d'outils boursiers."
    },
    {
        "ID": 19,
        "Article Link": "https://finance-heros.fr/trading-comment-devenir-trader/",
        "Article Title": "Trading : tout savoir pour se lancer ! (Guide 2025)",
        "Article Date": "2025-01-10",
        "Article Author Name": "Hugo Bompard",
        "Article Topics": "Trading, Guide, Débutants",
        "Article Main Domain": "Trading",
        "Article Source": "Finance Héros",
        "Article Content": "Ce guide complet explique les bases du trading, les différents types de titres financiers et fournit des conseils pour débuter efficacement dans le domaine."
    },
    {
        "ID": 20,
        "Article Link": "https://www.ig.com/fr/marche-actualites-et-idees-de-trading",
        "Article Title": "Actualités et idées de trading",
        "Article Date": "2025-02-05",
        "Article Author Name": "Valentin Aufrand",
        "Article Topics": "Trading, Actualités, Idées",
        "Article Main Domain": "Trading",
        "Article Source": "IG",
        "Article Content": "IG propose des analyses récentes sur les marchés financiers, offrant des idées de trading basées sur les tendances actuelles et les événements économiques."
    },

    
]

# Création du DataFrame
df = pd.DataFrame(articles)

# Enregistrer dans un sous-dossier du projet (ex: ./data/)
output_dir = "../data/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_path = os.path.join(output_dir, "articles.csv")

df.to_csv(csv_path, index=False, encoding="utf-8")

print(f"Le fichier dataset.csv a été généré avec succès dans : {csv_path}")
