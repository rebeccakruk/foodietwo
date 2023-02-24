from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import uuid
import bcrypt

@app.get('/api/client')
def get_client(token:str):
    # token = session.get("token")
    result = run_statement("CALL get_client(?)", [token])
    keys = ["clientId", "createdAt", "email", "firstName", "lastName", "username"]
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
    email = request.json.get("email")
    client_id = run_statement("CALL get_id(?)", [email])
    password = request.json.get("password")
    salt = bcrypt.gensalt()
    hash_result = bcrypt.hashpw(password.encode(), salt)

    
    

    #get procedure that grabs the hashed password and the id if it exists
    #then do pw verification if, else
    
    token = uuid.uuid4().hex
    keys = ["clientId", "token"]
    results = run_statement("CALL client_login(?, ?)", [client_id, token])
    if (type(results) == list):
    # check the row count here; 0 is not successful
            response = {
                        "clientId": client_id,
                        "token" : token
                        }
            return make_response(jsonify(response), 200)
    else:
        return "Something went wrong, please try again"

@app.post('/api/client')
def client_register():
    email = request.json.get("email")
    pw = request.json.get("password")
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
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
    elif "Duplicate entry" in results:
        return "This email is already registered, please login or register with another email."
    else:
        return "Something went wrong, please try again"