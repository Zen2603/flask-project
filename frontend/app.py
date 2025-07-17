from flask import Flask, render_template, request, flash, redirect
import requests
import os
import dotenv

dotenv.load_dotenv()
BACKEND_URL = 'http://192.168.56.101:9000'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/api')
def api():
    data = requests.get(f'{BACKEND_URL}/api')
    return data.json()

@app.route('/submit', methods=['POST'])
def submit():
    data = dict(request.form)

    if not data.get('name') or not data.get('email') or not data.get('feedback'):
        flash("All fields are required. Please fill in all fields.")
        return render_template('index.html')

    try:
        response = requests.post(f"{BACKEND_URL}/submit", json=data)
        response.raise_for_status()
        return render_template('success.html')
    
    except Exception as e:
        flash(f"something happed: {str(e)}")
        return render_template('index.html')
    
@app.route('/todo')
def todo():
    response = requests.get(f"{BACKEND_URL}/gettodoitems")
    items = response.json()
    return render_template('todo.html', items=items)

@app.route('/submittodoitem', methods=['POST', 'GET'])
def submittodoitem():
    data = dict(request.form)

    if not data.get('item_name') or not data.get('item_desc'):
        flash('Please fill in all fields')
        return redirect('todo')
    
    try:
        response = requests.post(f"{BACKEND_URL}/submittodoitem", json=data)
        response.raise_for_status()
    
    except Exception as e:
        flash(f"Something happedned : {e}")

    return redirect('todo')
    

if __name__ == "__main__":
    app.run(debug=True, host='192.168.56.101', port=8000)