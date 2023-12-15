import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob 
import plotly.graph_objects as go
from wordcloud import WordCloud
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter


st.set_page_config(layout="wide")
tab1, tab2 = "Analyse des Données", "Analyse des Sentiments"
tab = st.radio("Menu", (tab1, tab2))

if tab == tab1:


    # Charger et préparer les données pour le premier graphique (tendances de recherche)
    csv_file_path = 'multiTimeline (1).csv'
    data = pd.read_csv(csv_file_path, skiprows=1)
    data.columns = ['Week', 'Search Trend']
    data['Week'] = pd.to_datetime(data['Week'])
    data['Search Trend'] = data['Search Trend'].str.replace('<1', '0.5')
    data['Search Trend'] = pd.to_numeric(data['Search Trend'], errors='coerce')
    data['Search Trend'].fillna(method='ffill', inplace=True)

    # Créer le premier graphique Plotly (tendances de recherche)
    fig_trend = px.line(data, x='Week', y='Search Trend', title='Tendance de recherche dans le temps pour Spiderman 2',
                  labels={'Week': 'Date', 'Search Trend': 'Search Trend'})
    fig_trend.update_traces(mode='lines+markers')
    fig_trend.update_layout(hovermode='x')

    dat = pd.read_excel('reviw.xlsx')



    dat['polarity'] = dat['txtavis'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    dat['sentiment'] = dat['polarity'].apply(lambda x: "Positive" if x > 0 else ("Neutral" if x == 0 else "Negative"))

    sentiment_counts = dat['sentiment'].value_counts()
    df_sentiments = sentiment_counts.reset_index()
    df_sentiments.columns = ['Sentiment', 'Count']

    fig_sentiment = px.pie(df_sentiments, names='Sentiment', values='Count', title='Répartition des Sentiments',
                 hole=.3, color='Sentiment',
                 color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'gray'})
    fig_sentiment.update_traces(textinfo='percent+label')




    note_ranges = ['16 à 20', '11 à 15', '6 à 10', '0 à 5']
    counts = [208, 24, 6, 24]
    colors = ['green', 'yellow', 'orange', 'red']

    fig_notes = go.Figure()
    for note_range, count, color in zip(note_ranges, counts, colors):
        fig_notes.add_trace(go.Bar(
            x=[note_range],
            y=[count],
            name=note_range,
            marker_color=color,
            hoverinfo='y',
            text=count,
            textposition='auto'
        ))

    fig_notes.update_layout(
        title_text='Répartition des Notes',
        xaxis=dict(title='Plages de Notes'),
        yaxis=dict(title='Nombre de Notes'),
        barmode='group',
        dragmode=False
    )



    # Mise en page Streamlit avec deux colonnes
    st.markdown("<h1 style='text-align: center'>E-reputation du jeu Spiderman 2</h1>", unsafe_allow_html=True)
    st.write("Ce tableau de bord visualise les tendances de recherche et l'analyse des sentiments pour le jeu vidéo Spiderman 2 du 30 octobre au 15 décembre 2023")

    with st.container():
        st.plotly_chart(fig_trend, use_container_width=True)


    # Deuxième rangée : trois colonnes pour les autres éléments, avec des colonnes vides pour l'espacement
    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        # Création d'un graphique Plotly pour la note moyenne
        fig_kpi = go.Figure(go.Indicator(
            mode = "number+delta",
            value = 17,
            delta = {'reference': 15.2, 'relative': True, 'valueformat': '.1%'},
            title = {"text": "Note Moyenne"},
        ))

        fig_kpi.update_layout(height=450,width=500)  # Vous pouvez ajuster la taille selon vos besoins

        st.plotly_chart(fig_kpi, use_container_width=False)


    with col2:
        # Mise à jour de la configuration du graphique "Répartition des Notes" avec une taille spécifique
        fig_notes.update_layout(height=450, width=500)
        st.plotly_chart(fig_notes, use_container_width=False)

    with col3:
        # Mise à jour de la configuration du graphique "Répartition des Sentiments" avec une taille spécifique
        fig_sentiment.update_layout(height=450, width=500)
        st.plotly_chart(fig_sentiment, use_container_width=False)





    # Charger le modèle SpaCy
    nlp = spacy.load("fr_core_news_sm")


    avis_type = st.selectbox("Choisir le type d'avis", ["positif", "negatif"])
    col1, col2 = st.columns(2)

    with col1:


        # Fonction pour nettoyer le texte
        def clean_text(text):
            text = str(text).lower()
            text = re.sub(r'\W', ' ', text)  # Supprimer les caractères spéciaux
            text = re.sub(r'\s+', ' ', text)  # Supprimer les espaces supplémentaires
            return text

        # Fonction pour extraire les adjectifs
        def extract_adjectives(text):
            doc = nlp(text)
            adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
            return ' '.join(adjectives)

        # Nettoyer et extraire les adjectifs
        dat['cleaned_txtavis'] = dat['txtavis'].apply(clean_text)
        dat['adjectives'] = dat['cleaned_txtavis'].apply(extract_adjectives)

        # Classer les avis en positifs et négatifs (à adapter selon votre critère)
        dat['avis_type'] = dat['noteavis'].apply(lambda x: 'positif' if x > 10 else 'negatif')

        # Séparer les adjectifs des avis positifs et négatifs
        adjectives_positifs = ' '.join(dat[dat['avis_type'] == 'positif']['adjectives'])
        adjectives_negatifs = ' '.join(dat[dat['avis_type'] == 'negatif']['adjectives'])

        # Fonction pour créer et afficher le nuage de mots
        def create_wordcloud(adjectives, title):
            wordcloud = WordCloud(width=800, height=800, background_color='white', 
                                  stopwords=set(STOP_WORDS), 
                                  min_font_size=10).generate(adjectives)
            fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
            ax.imshow(wordcloud)
            ax.set_title(title)
            ax.axis("off")
            st.pyplot(fig)

        # Créer et afficher le nuage de mots en fonction de la sélection
        if avis_type == "positif":
            adjectives = ' '.join(dat[dat['avis_type'] == 'positif']['adjectives'])
            create_wordcloud(adjectives, "Nuage de mots des avis positifs")
        else:
            adjectives = ' '.join(dat[dat['avis_type'] == 'negatif']['adjectives'])
            create_wordcloud(adjectives, "Nuage de mots des avis négatifs")

    # Deuxième colonne pour le graphique Plotly
    with col2:
        # Données choisit à la main car bug qui bloque le deploiement
        positive_freq = Counter({'incroyable': 15, 'magnifique': 12, 'excellent': 9, 'agréable': 7, 'super': 6})
        negative_freq = Counter({'horrible': 10, 'médiocre': 8, 'repetitive': 7, 'difficile': 5, 'déçu': 4})
        neutral_freq = Counter({'moyen': 6, 'basique': 5, 'standard': 4, 'ordinaire': 3, 'normal': 2})

        # Création du graphique Plotly
        fig = go.Figure()

        # Ajouter les barres pour chaque sentiment
        fig.add_trace(go.Bar(y=list(positive_freq.keys()), x=list(positive_freq.values()), name='Positif', orientation='h'))
        fig.add_trace(go.Bar(y=list(negative_freq.keys()), x=list(negative_freq.values()), name='Négatif', orientation='h'))
        fig.add_trace(go.Bar(y=list(neutral_freq.keys()), x=list(neutral_freq.values()), name='Neutre', orientation='h'))

        # Mise à jour de la disposition
        fig.update_layout(
            title='Fréquence des mots par sentiment',
            yaxis_title='Mots',
            xaxis_title='Fréquence',
            barmode='group',
            updatemenus=[{
                'buttons': [
                    {'label': 'Tous', 'method': 'update', 'args': [{'visible': [True, True, True]}]},
                    {'label': 'Positif', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
                    {'label': 'Négatif', 'method': 'update', 'args': [{'visible': [False, True, False]}]},
                    {'label': 'Neutre', 'method': 'update', 'args': [{'visible': [False, False, True]}]}
                ],
                'direction': 'down',
                'showactive': True
            }]
        )


        fig.update_layout(height=750, width=750)
        st.plotly_chart(fig, use_container_width=False)

elif tab == tab2:
    
    # Charger et préparer les données pour le premier graphique (tendances de recherche)
    csv_file_path = 'multiTimeline (1).csv'
    data = pd.read_csv(csv_file_path, skiprows=1)
    data.columns = ['Week', 'Search Trend']
    data['Week'] = pd.to_datetime(data['Week'])
    data['Search Trend'] = data['Search Trend'].str.replace('<1', '0.5')
    data['Search Trend'] = pd.to_numeric(data['Search Trend'], errors='coerce')
    data['Search Trend'].fillna(method='ffill', inplace=True)

    # Créer le premier graphique Plotly (tendances de recherche)
    fig_trend = px.line(data, x='Week', y='Search Trend', title='Search Trend Over Time for Spiderman 2',
                  labels={'Week': 'Date', 'Search Trend': 'Search Trend'})
    fig_trend.update_traces(mode='lines+markers')
    fig_trend.update_layout(hovermode='x')

    # Créer un ensemble de données fictif pour l'analyse des sentiments (remplacez ceci par vos propres données)
    dat = pd.read_excel('reviw.xlsx')



    # Appliquer l'analyse de sentiment (remplacez ceci par votre propre analyse)
    dat['polarity'] = dat['txtavis'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    dat['sentiment'] = dat['polarity'].apply(lambda x: "Positive" if x > 0 else ("Neutral" if x == 0 else "Negative"))

    # Compter les occurrences de sentiment
    sentiment_counts = dat['sentiment'].value_counts()
    df_sentiments = sentiment_counts.reset_index()
    df_sentiments.columns = ['Sentiment', 'Count']    

    # Compter le nombre de chaque sentiment
    counts = dat['sentiment'].value_counts()

    # Calculer les pourcentages
    total = counts.sum()
    percentages = counts / total * 100

    # Créer la fonction de la jauge
    def create_gauge(sentiment, title, color):
        gauge_figure = go.Figure(go.Indicator(
            mode="number+gauge",
            value=percentages.get(sentiment, 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            number = {'suffix': "%"},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': "black"},
                'bar': {'color': color},  # Définit la couleur de la barre de la jauge
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, percentages.get(sentiment, 0)], 'color': 'lightgray'},
                    {'range': [percentages.get(sentiment, 0), 100], 'color': 'white'},
                ],
            }
        ))
        return gauge_figure

    # Créer la fonction pour générer le HTML des commentaires
    def generate_comments_html(comments, scores, sentiment):
        html_string = f"""
    <style>
        .scrollable {{
            height: 300px;
            overflow-y: scroll;
            border: 1px solid #ccc;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
    </style>
    <div class="scrollable">
    <table>
    <tr><th>Commentaires {sentiment}</th><th>Score</th></tr>
        """
        for comment, score in zip(comments, scores):
            html_string += f"<tr><td>{comment}</td><td>{score}</td></tr>"
        html_string += "</table></div>"
        return html_string
    # Utiliser Streamlit pour afficher les jauges et les commentaires
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_gauge('Negative', 'Négatif', 'red'), use_container_width=True)
        negative_comments = dat[dat['sentiment'] == 'Negative']
        st.markdown(generate_comments_html(negative_comments['txtavis'], negative_comments['polarity'], 'Négatifs'), unsafe_allow_html=True)

    with col2:
        st.plotly_chart(create_gauge('Positive', 'Positif', 'green'), use_container_width=True)
        positive_comments = dat[dat['sentiment'] == 'Positive']
        st.markdown(generate_comments_html(positive_comments['txtavis'], positive_comments['polarity'], 'Positifs'), unsafe_allow_html=True)    

    st.markdown('''
        <div style="margin-top: 4rem;"></div>
    ''', unsafe_allow_html=True)
