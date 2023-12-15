# Analyse E-reputation du jeu Spiderman 2 avec Streamlit

Cette application Streamlit vise à visualiser et analyser les tendances de recherche et l'opinion publique sur le jeu vidéo Spiderman 2. Elle utilise des graphiques interactifs et des analyses de sentiment pour fournir une vue d'ensemble de la réputation en ligne du jeu.

## Application dans le cloud

**Lien** : https://e-reput-spiderman2.streamlit.app/

## Fonctionnalités

L'application offre les fonctionnalités suivantes :

- **Analyse des tendances de recherche** : Visualisation des tendances de recherche sur une période spécifique à l'aide de graphiques interactifs.
- **Analyse des sentiments** : Évaluation des sentiments (positifs, négatifs, neutres) exprimés dans les avis utilisateurs, avec une répartition graphique et des détails textuels.
- **Répartition des notes** : Présentation des notes attribuées au jeu, visualisée sous forme de barres colorées.

## Installation et exécution

Pour exécuter cette application, vous devez installer les dépendances suivantes :

```bash
pip install streamlit pandas plotly textblob spacy wordcloud matplotlib
```

Assurez-vous également d'avoir installé le modèle `fr_core_news_sm` pour SpaCy :

```bash
python -m spacy download fr_core_news_sm
```

Pour lancer l'application, exécutez :

```bash
streamlit run str.py
```

Remplacez `str.py` par le nom de votre fichier script en cas de changement de nom.

## Structure du script

Le script est organisé en plusieurs sections principales :

- **Configuration de la page Streamlit** : Mise en place de l'interface utilisateur et navigation entre les onglets d'analyse.
- **Chargement et préparation des données** : Importation des données à partir de fichiers CSV et Excel, et prétraitement pour l'analyse.
- **Création de visualisations** : Utilisation de Plotly et Matplotlib pour générer des graphiques interactifs.
- **Analyse de texte** : Utilisation de TextBlob et SpaCy pour l'analyse de sentiment et la génération de nuages de mots.

## Source des données

Les données utilisées pour cette analyse proviennent de fichiers CSV et Excel (`multiTimeline (1).csv` et `reviw.xlsx`). Ces fichiers doivent être présents dans le même répertoire que le script pour le bon fonctionnement de l'application.

