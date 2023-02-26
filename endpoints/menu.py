from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/menu')
def add_to_menu():
    token = request.json.get("token")
    result = run_statement("CALL get_resto_id_with_token(?)", [token])
    if token == None:
        return "You are not logged in. Please login to add menu items."
    if (type(result) == list):
        resto_id = result[0][0]
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    image_url = request.json.get("imageUrl")
    result = run_statement("CALL add_menu_item(?, ?, ?, ?, ?, ?)", [resto_id, name, description, price, image_url])
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