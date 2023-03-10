from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/restaurant')
def resto_register():
    name = request.json.get("name")
    address = request.json.get("address")
    banner_url = request.json.get("bannerUrl")
    bio = request.json.get("bio")
    city = request.json.get("city")
    email = request.json.get("email")
    phone = request.json.get("phoneNum")
    pw = request.json.get("password")
    if pw == None:
        return "You must choose a password to complete registration."
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
    profile_url = request.json.get("profileUrl")
    token = uuid.uuid4().hex
    keys = ["restaurantId", "token"]
    response = []
    results = run_statement("CALL new_restaurant(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, address, bio, city, email, password, phone, banner_url, profile_url, token])
    if (type(results) == list):
        for data in results:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    elif "Column 'name' cannot be null" in results:
        return "Your restaurant must have a name. Please enter the name of your restaurant."
    elif "Column 'address' cannot be null" in results:
        return "Please enter the address of your restaurant."
    elif "Column 'bio' cannot be null" in results:
        return "Please enter a brief bio or description of your restaurant."
    elif "Column 'city' cannot be null" in results:
        return "Please enter the city of your restaurant."
    elif "for key 'restaurant_UN_email'" in results:
        return "This email is already registered, please login or register with another email."
    elif "for key 'restaurant_UN_username'" in results:
        return "This username is already taken, please choose another username."
    else:
        return "Something went wrong, please try again"
    
@app.get('/api/restaurant')
def get_restaurant():
    resto_id = request.args.get("restaurantId")
    response = []
    keys = ["name", "address", "bannerUrl", "bio", "city", "email", "phoneNum", "profileUrl", "restaurantId"]
    result = run_statement("CALL get_all_restaurants(?)", [resto_id])
    if (type(result) == list):
        for restaurant in result:
            response.append(dict(zip(keys, restaurant)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)
    
@app.patch('/api/restaurant')
def update_restaurant():
    token = request.json.get("token")
    result = run_statement("CALL get_resto_id_with_token(?)", [token])
    if token == None:
        return "You are not logged in. Please login to update your restaurant information."
    if (type(result) == list):
        restaurant_id = result[0][0]
    name = request.json.get("name")
    address = request.json.get("address")
    banner_url = request.json.get("bannerUrl")
    bio = request.json.get("bio")
    city = request.json.get("city")
    phone = request.json.get("phoneNum")
    profile_url = request.json.get("profileUrl")
    result = run_statement("CALL update_resto(?, ?, ?, ?, ?, ?, ?, ?)", [restaurant_id, name, address, banner_url, bio, city, phone, profile_url])
    if result == None:
        return "You have successfully updated your restaurant profile"
    elif "Data too long for column 'username_input'" in result:
        return "Your username is too long. Please choose another username. (maximum 100 characters)"
    elif "Data too long for column 'first_name_input' at row 0" in result:
        return "Your first name is too long, please check your entry and try again. (maximum 50 characters)"
    elif "Data too long for column 'last_name_input' at row 0" in result:
        return "Your last name is too long, please check your entry and try again. (maximum 50 characters)"
    else:
        return "Please try again"
