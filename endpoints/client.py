from app import app
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import uuid

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
        return "Something went wrong, please try again"

@app.post('/api/client')
def client_register():
    email = request.json.get("email")
    password = request.json.get("password")
    firstName = request.json.get("first_name")
    lastName = request.json.get("last_name")
    username = request.json.get("username")
    token = uuid.uuid4().hex
    # pictureUrl = request.json.get("pictureUrl")
    keys = ["clientId", "token"]
    response = []
    results = run_statement("CALL new_client(?, ?, ?, ?, ?, ?)", [email, password, firstName, lastName, username, token])
    # results = run_statement("CALL new_client(?, ?, ?, ?, ?, ?, ?)", [token, email, username, firstName, lastName, password, pictureUrl])
    if (type(results) == list):
        for data in results:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    else:
        return "Something went wrong, please try again"