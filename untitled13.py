# -*- coding: utf-8 -*-
"""Untitled13.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11T62PkZOBlTQIkViOpIEpM2Lp1V1k5gE
"""

import numpy as np
import pandas as pd

movies = pd.read_csv('/content/tmdb_5000_movies.csv.zip')
credits = pd.read_csv('/content/tmdb_5000_credits.csv.zip')

movies.head(1)

credits.head(1)

movies = movies.merge(credits,on= 'title')

movies.head(1)

credits.shape

# genres
# id
# keywords
# title
# overview
movies = movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.info()

movies.head()

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

movies.iloc[0].genres

#[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
# {'Action','Adventure','FFantasy','Scifi'}





import ast

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)
movies.head()

movies['keywords'] = movies['keywords'].apply(convert)
movies.head()

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L

movies['cast'] = movies['cast'].apply(convert)
movies.head()

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" "," ") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" "," ") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" "," ") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" "," ") for i in x])

movies.head()

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

new_df = movies[['movie_id','title','tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

new_df

new_df['tags'][0]

new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

new_df.head()



from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new_df['tags']).toarray()

vector.shape

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)

similarity

new_df[new_df['title'] == 'The Lego Movie'].index[0]

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def  stem(text) :
  y = []
  for i in text.split():
   y.append(ps.stem(i))
   return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

stem('In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. Action Adventure Fantasy Science Fiction culture clash future space war space colony society space travel futuristic romance space alien tribe alien planet cgi marine soldier battle love affair anti war power relations mind and soul 3d Sam Worthington Zoe Saldana Sigourney Weaver Stephen Lang Michelle Rodriguez Giovanni Ribisi Joel David Moore CCH Pounder Wes Studi Laz Alonso Dileep Rao Matt Gerald Sean Anthony Moran Jason Whyte Scott Lawrence Kelly Kilgour James Patrick Pitt Sean Patrick Murphy Peter Dillon Kevin Dorman Kelson Henderson David Van Horn Jacob Tomuri Michael Blain-Rozgay Jon Curry Luke Hawker Woody Schultz Peter Mensah Sonia Yee Jahnel Curfman Ilram Choi Kyla Warren Lisa Roumain Debra Wilson Chris Mala Taylor Kibby Jodie Landau Julie Lamm Cullen B. Madden Joseph Brady Madden Frankie Torres Austin Wilson Sara Wilson Tamica Washington-Miller Lucy Briant Nathan Meister Gerry Blair Matthew Chamberlain Paul Yates Wray Wilson James Gaylyn Melvin Leno Clark III Carvon Futrell Brandon Jelkes Micah Moch Hanniyah Muhammad Christopher Nolen Christa Oliver April Marie Thomas Bravita A. Threatt Colin Bleasdale Mike Bodnar Matt Clayton Nicole Dionne Jamie Harrison Allan Henry Anthony Ingruber Ashley Jeffery Dean Knowsley Joseph Mika-Hunt Terry Notary Kai Pantano Logan Pithyou Stuart Pollock Raja Gareth Ruck Rhian Sheehan T. J. Storm Jodie Taylor Alicia Vela-Bailey Richard Whiteside Nikie Zambo Julene Renee James Cameron')

vector[0]

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

recommend('Gandhi')

import pickle

pickle.dump(new_df,open('movie_list.pkl','wb'))

pickle.dump(new_df.to_dict() , open('movies_dict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))