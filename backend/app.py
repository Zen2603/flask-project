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

collection2 = db['todo-data']

@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    data = request.json
    print(data)
    try:
        collection2.insert_one(data)
        return "success"
    except Exception as e:
        return jsonify({"error" : "An unexpected error occurred", "details": str(e)}), 500

@app.route('/gettodoitems', methods=['POST', 'GET'])
def gettodoitems():
    items = list(collection2.find({}, {"_id": 0}))
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True, host='192.168.56.101', port=9000)