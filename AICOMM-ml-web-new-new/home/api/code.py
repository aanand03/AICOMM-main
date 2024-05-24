
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
nltk.download('stopwords')




df = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')

for column in ["Class Name","Review Text"]:
    df = df[df[column].notnull()]
df.drop(df.columns[0], inplace=True, axis=1)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

ps = PorterStemmer()

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

def preprocessing(data):
    txt = data.str.lower().str.cat(sep=' ') #1
    words = tokenizer.tokenize(txt) #2
    words = [w for w in words if not w in stop_words] #3
    return words

nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Pre-Processing
SIA = SentimentIntensityAnalyzer()
df['Review Text']= df['Review Text'].astype(str)

# Applying Model, Variable Creation
df['Polarity Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['compound'])
df['Neutral Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['neu'])
df['Negative Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['neg'])
df['Positive Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['pos'])

# Converting 0 to 1 Decimal Score to a Categorical Variable
df['Sentiment'] = ''
df.loc[df['Polarity Score'] > 0, 'Sentiment'] = 'Positive'
df.loc[df['Polarity Score'] == 0, 'Sentiment'] = 'Neutral'
df.loc[df['Polarity Score'] < 0, 'Sentiment'] = 'Negative'

df_recommended=df[(df['Sentiment']=='Positive')]
df_not_recommended=df[(df['Sentiment']=='Negative') | (df['Sentiment']=='Neutral')]

df_recommended=df_recommended.drop(['Age', 'Title', 'Recommended IND', 'Positive Feedback Count', 'Division Name', 'Neutral Score', 'Negative Score', 'Positive Score', 'Sentiment'], axis=1)

df_recommended=df_recommended.dropna(subset=['Clothing ID'])

df_sweaters=df_recommended[df_recommended['Class Name']=='Sweaters']
df_dresses=df_recommended[df_recommended['Class Name']=='Dresses']
df_jackets=df_recommended[df_recommended['Class Name']=='Jackets']
df_jeans=df_recommended[df_recommended['Class Name']=='Jeans']
df_knits=df_recommended[df_recommended['Class Name']=='Knits']
df_pants=df_recommended[df_recommended['Class Name']=='Pants']
df_skirts=df_recommended[df_recommended['Class Name']=='Skirts']

df_pants_filtered=df_pants.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_pants_filtered = df_pants_filtered[df_pants_filtered['Polarity Score'] > 0.9]
df_skirts_filtered=df_skirts.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_skirts_filtered = df_skirts_filtered[df_skirts_filtered['Polarity Score'] > 0.87]
df_jeans_filtered=df_jeans.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_jeans_filtered = df_jeans_filtered[df_jeans_filtered['Polarity Score'] > 0.83]
df_sweaters_filtered=df_sweaters.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_sweaters_filtered = df_sweaters_filtered[df_sweaters_filtered['Polarity Score'] > 0.82]
df_knits_filtered=df_knits.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_knits_filtered = df_knits_filtered[df_knits_filtered['Polarity Score'] > 0.84]
df_dresses_filtered=df_dresses.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_dresses_filtered = df_dresses_filtered[df_dresses_filtered['Polarity Score'] > 0.83]
df_jackets_filtered=df_jackets.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
df_jackets_filtered = df_jackets_filtered[df_jackets_filtered['Polarity Score'] > 0.75]

df_pants_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_skirts_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_jeans_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_sweaters_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_knits_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_dresses_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)
df_jackets_filtered.rename(columns = {'Clothing ID':'clothing_id', 'Class Name':'class_name', 'Polarity Score':'polarity_score'}, inplace = True)

df_pants_filtered.to_json("pants.json", orient='records')
df_skirts_filtered.to_json("skirts.json", orient='records')
df_jeans_filtered.to_json("jeans.json", orient='records')
df_sweaters_filtered.to_json("sweaters.json", orient='records')
df_knits_filtered.to_json("knits.json", orient='records')
df_dresses_filtered.to_json("dresses.json", orient='records')
df_jackets_filtered.to_json("jackets.json", orient='records')