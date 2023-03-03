from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement

@app.post('/api/order')
def new_order():
    token = request.json.get("token")
    restaurant_id = request.json.get("restaurantId")
    order = request.json.get("items")
    result = run_statement("CALL get_client(?)", [token])
    if token == None:
        return "You are not logged in. Please login to review your information."
    if (type(result) == list):
        client_id = result[0][0]
        result = run_statement("CALL new_order(?, ?)", [client_id, restaurant_id])
        if (type(result) == list): 
            order_id = result[0][0]
            for item in order:
                items = item
                result = run_statement("CALL order_items(?, ?)", [items, order_id])
    if result == None:
        return "Item added successfully."
    else:
        return make_response(jsonify(result), 500)

@app.get('/api/order')
def get_orders():
    token = request.json.get("token")
    order_id = request.args.get("orderId")
    response = []
    result = run_statement("CALL check_token(?)", [token])
    client_id = result[0][0]
    client_login_check = result[0][1]
    restaurant_id = result [1][0]
    resto_login_check = result[1][0]
    if client_login_check > 1 and restaurant_id == None:
        if order_id != None:
            validate_order = run_statement("CALL check_order(?, ?)", [client_id, order_id])
            order_exists = validate_order[0][0]
            if order_exists == 0:
                return f"You don't have any orders with id {order_id}. Please check your orders and try again."
            result = run_statement("CALL get_order(?, ?)", [order_id, client_id])
            if (type(result) == list):
                current_order = {}
                for item in result:
                    current_order["clientId"] = item[0]
                    current_order["createdAt"] = item[1]
                    current_order["orderId"] = item[6]
                    current_order["isCancelled"] = bool(item[2])
                    current_order["isComplete"] = bool(item[3])
                    current_order["isConfirmed"] = bool(item[4])
                    current_order["items"] = [
                        item[5]
                    ]
                    current_order["restaurantId"] = item[7]
                    if response != [] and item[6] == response[-1]["orderId"]:
                        response[-1]["items"].append(item[5])
                    else:
                        response.append(current_order)
                        current_order = {}
                return make_response(jsonify(response), 200)
        if order_id == None:
            result = run_statement("CALL get_order(?, ?)", [order_id, client_id])
            if (type(result) == list):
                current_order = {}
                for item in result:
                    current_order["clientId"] = item[0]
                    current_order["createdAt"] = item[1]
                    current_order["orderId"] = item[6]
                    current_order["isCancelled"] = bool(item[2])
                    current_order["isComplete"] = bool(item[3])
                    current_order["isConfirmed"] = bool(item[4])
                    current_order["items"] = [
                        item[5]
                    ]
                    current_order["restaurantId"] = item[7]
                    if response != [] and item[6] == response[-1]["orderId"]:
                        response[-1]["items"].append(item[5])
                    else:
                        response.append(current_order)
                        current_order = {}
                return make_response(jsonify(response), 200)
    elif "Incorrect integer value" in result:
        return "Please enter order ID number"
    else:
        return make_response(jsonify(response), 500)

@app.patch('/api/order')
def update_order():
    token = request.json.get("token")
    order_id = request.json.get("orderId")
    cancel_order = request.json.get("cancelOrder")
    confirm_order = request.json.get("confirmOrder")
    complete_order = request.json.get("completeOrder")
    result = run_statement("CALL check_token(?)", [token])
    client_id = result[0][0]
    client_login_check = result[0][1]
    restaurant_id = result [1][0]
    resto_login_check = result[1][0]
    if client_login_check > 1 and restaurant_id == None:
        validate_order = run_statement("CALL check_order(?, ?, ?)", [client_id, restaurant_id, order_id])
        if (type(validate_order) == list):
            validate_order = result [0][0]
            if validate_order < 1:
                return f"You don't have any orders with id {order_id}. Please check your orders and try again."
        result = run_statement("CALL update_order(?, ?, ?, ?, ?, ?)", [client_id, order_id, restaurant_id, cancel_order, confirm_order, complete_order])
        if result == None:
            return "You have successfully cancelled your order."
    elif client_login_check < 1 and resto_login_check > 1:
        validate_order = run_statement("CALL check_order(?, ?, ?)", [client_id, restaurant_id, order_id])
        if (type(validate_order) == list):
            validate_order = result [0][0]
            if validate_order < 1:
                return f"You don't have any orders with id {order_id}. Please check your orders and try again."
        result = run_statement("CALL update_order(?, ?, ?, ?, ?, ?)", [client_id, order_id, restaurant_id, cancel_order, confirm_order, complete_order])
        if result == None:
            return "You have successfully cancelled your order."
    else:
        return "Something went wrong. Please try again."
