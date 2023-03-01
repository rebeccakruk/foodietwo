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
    items = []
    keys = ["clientId",
        "createdAt",
        "isCancelled",
        "isComplete",
        "isConfirmed",
        "items",
        "orderId",
        "restaurantId"]
    result = run_statement("CALL get_client(?)", [token])
    if token == None:
        return "You are not logged in. Please login to review see your orders."
    if (type(result) == list):
        client_id = result[0][0]
        result = run_statement("CALL get_order(?, ?)", [order_id, client_id])
        if (type(result) == list):
            for data in result:
                response.append(dict(zip(keys, data)))
    result = run_statement("CALL get_menu_items(?)", [order_id])
    if (type(result) == list):
        for item in result:
            items.extend(item)
    response.insert(4, items)
    print(response)
    return make_response(jsonify(response), 200)
