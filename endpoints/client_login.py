from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

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
        if results[0][0] == 1:            
            response = {
                        "clientId": client_id,
                        "token" : token
                        }
            return make_response(jsonify(response), 200)
    else:
        return "Please provide a valid password"
    
@app.delete('/api/client-login')
def logout_client():
    token = request.json.get("token")
    result = run_statement("CALL get_session_id(?)", [token])
    if token == None:
        return "You are already signed out."
    elif result == []:
        return "You are already signed out."
    elif (type(result) == list):
        id = result[0][0]
    result = run_statement("CALL logout_client(?)", [id])
    if result == None:
        return "Sign out successful."
    else:
        return "Please try again."