import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download(['stopwords', 'wordnet', 'omw-1.4'])

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':',
                  ';', '(', ')', '[', ']', '{', '}'])

food = pd.read_csv('food_data.csv', encoding='latin-1')
resto = pd.read_csv('restaurant_data.csv', encoding='latin-1')
resto = resto.loc[(resto['Country Code'] == 94) & (resto['City'] == 'Jakarta'), :]
resto = resto.loc[resto['Longitude'] != 0, :]
resto = resto.loc[resto['Latitude'] != 0, :]
resto = resto.loc[resto['Latitude'] < 29]
resto = resto.loc[resto['Rating text'] != 'Not rated']
resto['Cuisines'] = resto['Cuisines'].astype(str)

food_to_cuisine_map = {
    "japanese": "japanese",
    "korean": "korean",
    "sunda": "sunda",
    "indonesian": "indonesian",
    "peranakan": "peranakan",
    "burger": "burger",
    "italian": "italian",
    "cafe": "cafe",
    "seafood": "seafood",
    "western food": "western food",
    "desserts": "desserts",
    "bakery": "bakery",
    "coffee and tea": "coffee and tea",
    "cafe": "italian",
    "ramen": "japanese",
    "pizza": "pizza",
}

def search_comfort(mood):
    lemmatizer = WordNetLemmatizer()
    foodcount = {}
    for i in range(124):
        temp = [temps.strip().replace('.', '').replace(',', '').lower() for temps in str(
            food["comfort_food_reasons"][i]).split(' ') if temps.strip() not in stop_words]
        if mood in temp:
            foodtemp = [lemmatizer.lemmatize(temps.strip().replace('.', '').replace(',', '').lower(
            )) for temps in str(food["comfort_food"][i]).split(',') if temps.strip() not in stop_words]
            for a in foodtemp:
                if a not in foodcount.keys():
                    foodcount[a] = 1
                else:
                    foodcount[a] += 1
    sorted_food = []
    sorted_food = sorted(foodcount, key=foodcount.get, reverse=True)
    return sorted_food


def find_my_comfort_food(mood):
    topn = []
    topn = search_comfort(mood)
    return topn[:3]
