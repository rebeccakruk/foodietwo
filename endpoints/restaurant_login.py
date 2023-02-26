from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import uuid
import bcrypt

@app.post('/api/restaurant-login')
def login_restaurant():
    email = request.json.get("email")
    #get procedure that grabs the hashed password and the id if it exists
    result = run_statement("CALL get_resto_id(?)", [email])
    if (result == []):
        return "Please enter a valid email or register as a new restaurant"
    if (type(result) == list):
        password = result[0][1]
        restaurant_id = result[0][0]
    pw1 = password.encode('utf-8')
    #then do pw verification if, else
    password2 = request.json.get("password")
    if (bcrypt.checkpw(password2.encode(), pw1)):
        token = uuid.uuid4().hex
        results = run_statement("CALL resto_login(?, ?)", [token, restaurant_id])
        if results[0][0] == 1:            
            response = {
                        "restaurantId": restaurant_id,
                        "token" : token
                        }
            return make_response(jsonify(response), 200)
    else:
        return "Please provide a valid password"
    
@app.delete('/api/restaurant-login')
def logout_restaurant():
    token = request.json.get("token")
    result = run_statement("CALL get_resto_session_id(?)", [token])
    if token == None:
        return "You are already signed out."
    elif result == []:
        return "You are already signed out."
    elif (type(result) == list):
        id = result[0][0]
    result = run_statement("CALL logout_resto(?)", [id])
    if result == None:
        return "Sign out successful."
    else:
        return "Please try again."