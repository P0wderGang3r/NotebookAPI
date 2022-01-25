from flask import Flask, jsonify
from peewee import *
from dbclasses import *

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style = 'color:green'>Default route</h1>" +	"Routes: <br>" + "<li>/init_databases </li>" + "<li>[post] /user </li>" + "<li>[get] /todo </li>" +	"<li>[post] /todo </li>" + "<li>[delete] /todo/{id} </li>" + "<li>[put] /todo/{id} </li>"

@app.route("/test")
def test_route():
	return "Test_route"

@app.route("/init_databases", method=['POST'])
def init_databases():
	users.create_table()
	todos.create_table()
	return jsonify({'initiaized': 'initiaized'})

#post /user
@app.route("/user", method=['POST'])
def add_user():
	new_user = users(name = request.json['title'], password = request.json['password'], user_id = users.get())
	new_user.save()
	return jsonify(new_user.get(name): new_user.get(password)})


#get /todo
@app.route("/todo", method=['GET'])
def get_todo():
	return jsonify({'todo_get': 'todo_get'})

#post /todo
@app.route("/todo", method=['POST'])
def add_todo():
	if not request.json or not 'title' in request.json:
		abort(400)
	return jsonify({'initiaized': 'initiaized'})


#delete /todo/{id}
@app.route("/user", method=['DELETE'])
def delete_todo():
	return jsonify({'initiaized': 'initiaized'})


#put /todo/{id}
@app.route("/user", method=['PUT'])
def update_todo():
	return jsonify({'initiaized': 'initiaized'})


# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
