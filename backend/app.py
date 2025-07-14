from flask import Flask, request, jsonify
import requests
import os
import dotenv
from pymongo import MongoClient
import json

dotenv.load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri)

db = client.assignmentdb
collection = db['feedback-data']

app = Flask(__name__)

def load_data():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    return data

@app.route('/api')
def api():
    data = load_data()
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print(data)
    try:
        collection.insert_one(data)
        return "success"
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host='192.168.56.101', port=9000)