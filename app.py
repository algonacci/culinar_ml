from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    json = {
        "data": "Hello World",
        "message": "Success",
        "status_code": 200
    }
    return jsonify(json)

@app.route("/post", methods=["POST"])
def post():
    input = request.get_json()
    json = {
        "data": input,
        "message": "Success",
        "status_code": 200
    }
    return jsonify(json)

@app.errorhandler(404)
def not_found(error):
    json = {
        "data": "Error",
        "message": "Endpoint Not Found",
        "status_code": 404
    }
    return jsonify(json)

@app.errorhandler(500)
def server_error(error):
    json = {
        "data": "Error",
        "message": "Server Error",
        "status_code": 500
    }
    return jsonify(json)

if __name__ == "__main__":
    app.run(debug=True)