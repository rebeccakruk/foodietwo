from flask import Flask, make_response, jsonify, request
from dbcreds import production_mode
import json
from dbhelpers import run_statement, connect_db
import uuid

app = Flask(__name__)
connect_db()
@app.get('/api/client')
def get_client():
    result = run_statement("CALL get_client")
    keys = ["id", "created_at", "email", "firstName", "lastName", "pictureUrl", "username"]
    response = []
    if (type(result) == list):
        for client in result:
            print(response)
            response.append(dict(zip(keys, client)))
        return make_response(jsonify(response), 200)
    else:
        print(result)
        return make_response(jsonify(result), 500)
    
@app.post('/api/client-login')
def login_client():
    token = uuid.uuid4().hex
    email = request.json.get("email")
    password = request.json.get("password")
    keys = ["clientId", "token"]
    response = []
    results = run_statement("CALL client_login(?, ?, ?)", [email, password, token])
    if (type(results) == list):
        for data in results:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    else:
        return "oops"



if (production_mode == True):
    print("Running server in production mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
app.run(debug=True)