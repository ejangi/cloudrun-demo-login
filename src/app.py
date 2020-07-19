import os
from flask import Flask, request, jsonify, render_template
from google.oauth2 import id_token
import google.auth.transport.requests

app = Flask(__name__)
client_id = os.environ.get('CLIENT_ID', '')

def verify_token(req):
    authorization = req.headers.get('Authorization')
    if type(authorization) is not str:
        return False
    auth_items = authorization.split()

    if len(auth_items) != 2:
        return False
    token = auth_items[1]

    try:
        id_info = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), client_id)
        if id_info['iss'] == 'accounts.google.com' and len(id_info['sub']) > 0:
            return True
        return False
    except ValueError:
        return False


@app.route('/')
def index():
    title = 'Google Cloud Run Login Demo'
    return render_template('index.html', title = title, client_id = client_id)

@app.route('/api/hello')
def hello_world():
    if verify_token(request):
        return jsonify({"status":"ok", "message":"Hello world!"})
    else:
        return jsonify({"status":"error", "message":"Token verification failed."})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
