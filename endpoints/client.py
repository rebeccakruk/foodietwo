from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid
    
@app.post('/api/client')
def client_register():
    email = request.json.get("email")
    pw = request.json.get("password")
    if pw == None:
        return "You must choose a password to complete registration."
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
    if (type(results) == list):
        for data in results:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    elif "for key 'client_UN'" in results:
        return "This email is already registered, please login or register with another email."
    elif "for key 'client_UN_username'" in results:
        return "This username is already taken, please choose another username."
    elif "Column 'username' cannot be null" in results:
        return "Username cannot be blank. You must choose a username to register."
    elif "Column 'first_name' cannot be null" in results:
        return "First name cannot be blank. You must enter your first name to register."
    elif "Column 'last_name' cannot be null" in results:
        return "Last name cannot be blank. You must enter your last name to register."
    else:
        return "Something went wrong, please try again"

@app.get('/api/client')
def get_client():
    token = request.args.get("token")
    result = run_statement("CALL get_client(?)", [token])
    if token == None:
        return "You are not logged in. Please login to access your information."
    response = []
    keys = ["clientId", "createdAt", "email", "firstName", "lastName", "pictureUrl", "username"]
    if (type(result) == list):
        for client in result:
            response.append(dict(zip(keys, client)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)

@app.patch('/api/client')
def update_client():
    token = request.args.get("token")
    result = run_statement("CALL get_id_with_token(?)", [token])
    if token == None:
        return "You are not logged in. Please login to update your client information."
    if (type(result) == list):
        client_id = result[0][0]
    username = request.json.get("username")
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    pw = request.json.get("password")
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
    picture_url = request.json.get("pictureUrl")
    result = run_statement("CALL update_client(?, ?, ?, ?, ?, ?)", [client_id, username, first_name, last_name, password, picture_url])
    if result == None:
        return "You have successfully updated your client profile"
    elif "Data too long for column 'username_input'" in result:
        return "Your username is too long. Please choose another username. (maximum 100 characters)"
    elif "Data too long for column 'first_name_input' at row 0" in result:
        return "Your first name is too long, please check your entry and try again. (maximum 50 characters)"
    elif "Data too long for column 'last_name_input' at row 0" in result:
        return "Your last name is too long, please check your entry and try again. (maximum 50 characters)"
    else:
        return "Please try again"
    
@app.delete('/api/client')
def client_delete():
    token = request.args.get("token")
    result = run_statement("CALL get_id_with_token(?)", [token])
    if (type(result) == list):
        client_id = result[0][0]
    result = run_statement("CALL delete_client(?)", [client_id])
    if result == None:
        return "You've successfully deleted your account"
    else:
        return "Please try again"
    

