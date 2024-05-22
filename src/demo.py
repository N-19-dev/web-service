from flask import Flask, jsonify, abort
from main import User  # Replace with your actual model import path


app = Flask(__name__)

@app.route("/home", methods={"GET"})
def home():
    return "<h1>HELLO MI FIANDE<h1>"
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)

