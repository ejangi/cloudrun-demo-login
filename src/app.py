import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Google Cloud Run Login Demo'
    client_id = os.environ.get('CLIENT_ID', '')
    return render_template('index.html', title = title, client_id = client_id)

@app.route('/api/hello')
def hello_world():
    return jsonify({"status":"ok", "message":"Hello world!"})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
