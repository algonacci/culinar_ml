from flask import Flask, jsonify, request
from flask_cors import cross_origin
import numpy as np
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# nltk.download()

app = Flask(__name__)

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':',
                  ';', '(', ')', '[', ']', '{', '}'])

food = pd.read_csv('food_data.csv', encoding='latin-1')
resto = pd.read_csv('restaurant_data.csv', encoding='latin-1')
resto = resto.loc[(resto['Country Code'] == 94) &
                  (resto['City'] == 'Jakarta'), :]
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
    "café": "café",
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


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    json = {
        "data": "Hello World",
        "message": "Success",
        "status_code": 200
    }
    return jsonify(json)


@app.route("/find", methods=["POST"])
@cross_origin()
def find():
    restaurants_list = []
    input_request = request.get_json()
    mood = input_request["mood"]
    if request.method == "POST":
        if mood == "":
            json = {
                "data": "",
                "message": "Mood cannot be empty",
                "status_code": 400
            }
            return jsonify(json)
        else:
            topn = find_my_comfort_food(mood)
            for i in topn:
                restaurants = resto[resto.Cuisines.str.contains(food_to_cuisine_map[i], case=False)].sort_values(
                    by='Aggregate rating', ascending=False).head(3)
                restaurants_list.append(restaurants.iloc[0])
                restaurants_list.append(restaurants.iloc[1])
                restaurants_list.append(restaurants.iloc[2])

            resto_1 = restaurants_list[:3]
            resto_2 = restaurants_list[3:6]
            resto_3 = restaurants_list[6:9]

            for i in resto_1:
                name_1 = str(i['Restaurant Name'])
                rating_1 = str(i['Aggregate rating'])
                cuisine_1 = str(i['Cuisines'])
                average_price_1 = str(i['Average Cost for two'])
                rating_1 = str(i['Aggregate rating'])
                address_1 = str(i['Address'])
                latitude_1 = str(i['Latitude'])
                longitude_1 = str(i['Longitude'])

            for i in resto_2:
                name_2 = str(i['Restaurant Name'])
                rating_2 = str(i['Aggregate rating'])
                cuisine_2 = str(i['Cuisines'])
                average_price_2 = str(i['Average Cost for two'])
                rating_2 = str(i['Aggregate rating'])
                address_2 = str(i['Address'])
                latitude_2 = str(i['Latitude'])
                longitude_2 = str(i['Longitude'])

            for i in resto_3:
                name_3 = str(i['Restaurant Name'])
                rating_3 = str(i['Aggregate rating'])
                cuisine_3 = str(i['Cuisines'])
                average_price_3 = str(i['Average Cost for two'])
                rating_3 = str(i['Aggregate rating'])
                address_3 = str(i['Address'])
                latitude_3 = str(i['Latitude'])
                longitude_3 = str(i['Longitude'])

            json = {
                "data": {
                    "top_three_restaurants": topn,
                    "restaurants": {
                        "restaurant_1": {
                            "name": name_1,
                            "rating": rating_1,
                            "cuisine": cuisine_1,
                            "average_price": average_price_1,
                            "address": address_1,
                            "latitude": latitude_1,
                            "longitude": longitude_1
                        },
                        "restaurant_2": {
                            "name": name_2,
                            "rating": rating_2,
                            "cuisine": cuisine_2,
                            "average_price": average_price_2,
                            "address": address_2,
                            "latitude": latitude_2,
                            "longitude": longitude_2
                        },
                        "restaurant_3": {
                            "name": name_3,
                            "rating": rating_3,
                            "cuisine": cuisine_3,
                            "average_price": average_price_3,
                            "address": address_3,
                            "latitude": latitude_3,
                            "longitude": longitude_3
                        }
                    }
                },
                "message": "Success",
                "status_code": 200
            }
            return jsonify(json)
    else:
        json = {
            "data": "",
            "message": "Method not allowed",
            "status_code": 405
        }
        return jsonify(json)


@app.errorhandler(404)
@cross_origin()
def not_found(error):
    json = {
        "data": "Error",
        "message": "Endpoint Not Found",
        "status_code": 404
    }
    return jsonify(json)


@app.errorhandler(500)
@cross_origin()
def server_error(error):
    json = {
        "data": "Error",
        "message": "Server Error",
        "status_code": 500
    }
    return jsonify(json)


if __name__ == "__main__":
    app.run(debug=True)
