from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement

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
    result = run_statement("CALL add_menu_item(?, ?, ?, ?, ?)",  [name, description, price, image_url, resto_id])
    if result == None:
        return f"You have successfully added {name} to your menu!"
    elif "Data too long for column 'username_input'" in result:
        return "Your username is too long. Please choose another username. (maximum 100 characters)"
    elif "Data too long for column 'first_name_input' at row 0" in result:
        return "Your first name is too long, please check your entry and try again. (maximum 50 characters)"
    elif "Data too long for column 'last_name_input' at row 0" in result:
        return "Your last name is too long, please check your entry and try again. (maximum 50 characters)"
    else:
        return "Please try again"
    
@app.get('/api/menu')
def get_menu():
    resto_id = request.args.get("restaurantId")
    menu_id = request.args.get("menuId")
    response = []
    keys = ["description", "imageUrl", "menuId", "name", "price", "restaurantId"]
    if resto_id != None and menu_id == None:
        result = run_statement("CALL get_menu(?, ?)", [resto_id, menu_id])
        if (type(result) == list):
            for data in result:
                response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    if resto_id == None and menu_id != None:
        result = run_statement("CALL get_menu(?, ?)", [resto_id, menu_id])
        if (type(result) == list):
            for data in result:
                response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    if resto_id != None and menu_id != None:
        result = run_statement("CALL get_menu(?, ?)", [resto_id, menu_id])
        if result == []:
            selection = run_statement("CALL item_lookup(?, ?)", [resto_id, menu_id])
            if (type(selection) == list):
                food_name = selection[0][0]
                resto = selection[0][1]
            return f"Sorry, {food_name} is not listed on the menu at {resto}. Please refine your search."
        else:
            if (type(result) == list):
                keys = ["description", "imageUrl", "menuId", "name", "price", "restaurantId"]
                for data in result:
                    response.append(dict(zip(keys, data)))
                return make_response(jsonify(response), 200)
    if resto_id == None and menu_id == None:
        result = run_statement("CALL get_menu(?, ?)", [resto_id, menu_id])
        if (type(result) == list):
            for data in result:
                response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)

@app.patch('/api/menu')
def edit_menu():
    token = request.json.get("token")
    result = run_statement("CALL get_resto_id_with_token(?)", [token])
    if token == None:
        return "You are not logged in. Please login to delete items from the menu."
    if (type(result) == list):
        resto_id = result[0][0]
    menu_id = request.json.get("menuId")
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    image_url = request.json.get("imageUrl")
    result = run_statement("CALL edit_menu(?, ?, ?, ?, ?, ?)", [resto_id, menu_id, name, description, price, image_url])
    if result == None:
        return f"You've successfully updated {name} on your menu."
    else:
        return "Please try again."

@app.delete('/api/menu')
def delete_item():
    token = request.json.get("token")
    result = run_statement("CALL get_resto_id_with_token(?)", [token])
    if token == None:
        return "You are not logged in. Please login to delete items from the menu."
    if (type(result) == list):
        resto_id = result[0][0]
        menu_id = request.json.get("menuId")
        selection = run_statement("CALL get_menu(?, ?)", [resto_id, menu_id])
        if selection == []:
            option = run_statement("CALL item_lookup(?, ?)", [resto_id, menu_id])
            if (type(option) == list):
                food_name = option[0][0]
            return f"You cannot delete {food_name}; it is not from your restaurant. Please make another selection."
        elif (type(selection) == list):
            option = run_statement("CALL item_lookup(?, ?)", [resto_id, menu_id])
            if (type(option) == list):
                food_name = option[0][0]
            result = run_statement("CALL delete_menu_item(?, ?)", [menu_id, resto_id])
            if result == None:
                return f"You have successfully deleted {food_name} from your menu!"
    # elif "Data too long for column 'username_input'" in result:
    #     return "Your username is too long. Please choose another username. (maximum 100 characters)"
    # elif "Data too long for column 'first_name_input' at row 0" in result:
    #     return "Your first name is too long, please check your entry and try again. (maximum 50 characters)"
    # elif "Data too long for column 'last_name_input' at row 0" in result:
    #     return "Your last name is too long, please check your entry and try again. (maximum 50 characters)"
    else:
        return "Please try again"