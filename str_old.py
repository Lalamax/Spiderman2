import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob  # Remplacez ceci par votre propre analyse de sentiment
import plotly.graph_objects as go
from wordcloud import WordCloud
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter




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

# Créer le deuxième graphique Plotly (répartition des sentiments)
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

st.set_page_config(layout="wide")
#st.markdown("""
#    <style>
#    .stApp {
#        background-image: url("https://wallpapers.com/images/hd/spider-man-miles-morales-ps5-1ushde5atjy9e2w2.jpg");
#        background-size: cover;
#    }
#    </style>
#    """, unsafe_allow_html=True)



# Mise en page Streamlit avec deux colonnes
st.markdown("<h1 style='text-align: center'>E-reputation du jeu Spiderman 2</h1>", unsafe_allow_html=True)
st.write("Ce tableau de bord visualise les tendances de recherche et l'analyse des sentiments pour le jeu vidéo Spiderman 2 du 30 octobre au 15 décembre")

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

import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import pandas as pd
import re
from collections import Counter
import plotly.graph_objects as go

# Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_sm")

# Votre code pour charger et préparer le DataFrame 'dat'
# ...
avis_type = st.selectbox("Choisir le type d'avis", ["positif", "negatif"])
# Troisième rangée pour le sélecteur de nuage de mots et le graphique Plotly
col1, col2 = st.columns(2)

# Sélecteur pour choisir entre avis positifs et négatifs dans la première colonne
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
    # Exemple de données fictives pour le graphique
    positive_freq = Counter({'excellent': 15, 'bon': 12, 'parfait': 9, 'agréable': 7, 'super': 6})
    negative_freq = Counter({'mauvais': 10, 'horrible': 8, 'problème': 7, 'difficile': 5, 'déçu': 4})
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
