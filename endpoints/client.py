from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid
    
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
    pictureUrl = request.json.get("pictureUrl")
    keys = ["clientId", "token"]
    response = []
    results = run_statement("CALL new_client(?, ?, ?, ?, ?, ?, ?)", [email, password, firstName, lastName, username, token, pictureUrl])
    # results = run_statement("CALL new_client(?, ?, ?, ?, ?, ?, ?)", [token, email, username, firstName, lastName, password, pictureUrl])
    if (type(results) == list):
        for data in results:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    elif "Duplicate entry" in results:
        return "This email is already registered, please login or register with another email."
    else:
        return "Something went wrong, please try again"

@app.post('/api/client-login')
def login_client():
    email = request.json.get("email")
    #get procedure that grabs the hashed password and the id if it exists
    result = run_statement("CALL get_id(?)", [email])
    if (result == []):
        return "Please enter a valid email or register as a new client"
    if (type(result) == list):
        password = result[0][1]
        client_id = result[0][0]
    pw1 = password.encode('utf-8')
    #then do pw verification if, else
    password2 = request.json.get("password")
    if (bcrypt.checkpw(password2.encode(), pw1)):
        token = uuid.uuid4().hex
        results = run_statement("CALL client_login(?, ?)", [token, client_id])
    # check the row count here; 0 is not successful
        if results[0][0] == 1:            
            response = {
                        "clientId": client_id,
                        "token" : token
                        }
            return make_response(jsonify(response), 200)
    else:
        return "Please provide a valid password"

@app.get('/api/client')
def get_client():
    token = request.args.get("token")
    response = []
    keys = ["clientId", "createdAt", "email", "firstName", "lastName", "pictureUrl", "username"]
    result = run_statement("CALL get_client(?)", [token])
    if (type(result) == list):
        for client in result:
            print(response)
            response.append(dict(zip(keys, client)))
        return make_response(jsonify(response), 200)
    else:
        print(result)
        return make_response(jsonify(result), 500)

@app.patch('/api/client')
def update_client():
    token = request.args.get("token")
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    pw = request.json.get("password")
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
    picture_url = request.json.get("pictureUrl")
    result = run_statement("CALL update_client(?, ?, ?, ?, ?)", [token, first_name, last_name, password, picture_url])
    print(result)
