from flask import Flask, jsonify, request
from flask_cors import cross_origin
import module as md

app = Flask(__name__)

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
            topn = md.find_my_comfort_food(mood)
            for i in topn:
                restaurants = md.resto[md.resto.Cuisines.str.contains(md.food_to_cuisine_map[i], case=False)].sort_values(
                    by='Aggregate rating', ascending=False).head(3)
                restaurants_list.append(restaurants.iloc[0])
                restaurants_list.append(restaurants.iloc[1])
                restaurants_list.append(restaurants.iloc[2])

            resto = restaurants_list[:9]
            resto_list = []

            for i in resto:
                name = str(i['Restaurant Name'])
                rating = str(i['Aggregate rating'])
                cuisine = str(i['Cuisines'])
                average_price = str(i['Average Cost for two'])
                rating = str(i['Aggregate rating'])
                address = str(i['Address'])
                latitude = str(i['Latitude'])
                longitude = str(i['Longitude'])
                image_url = str(i['image_url'])
                resto_list.append({"name": name, "rating": rating, "cuisine": cuisine, "average_price": average_price,
                                  "address": address, "latitude": latitude, "longitude": longitude, "image_url": image_url})

            json = {
                "data": {
                    "top_three_restaurants": topn,
                    "restaurants": {
                        "restaurant_1": resto_list[0],
                        "restaurant_2": resto_list[1],
                        "restaurant_3": resto_list[2],
                        "restaurant_4": resto_list[3],
                        "restaurant_5": resto_list[4],
                        "restaurant_6": resto_list[5],
                        "restaurant_7": resto_list[6],
                        "restaurant_8": resto_list[7],
                        "restaurant_9": resto_list[8]
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
