from flask import Flask, jsonify, request
from peewee import *
from dbclasses import *
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style = 'color:green'>Default route</h1>" +	"Routes: <br>" + "<li>/init_databases </li>" + "<li>[post] /user </li>" + "<li>[get] /todo </li>" +	"<li>[post] /todo </li>" + "<li>[delete] /todo/{id} </li>" + "<li>[put] /todo/{id} </li>"

@app.route("/test")
def test_route():
	return "Test_route"

@app.route("/init_databases", methods=['POST'])
def init_databases():
	users.create_table()
	todos.create_table()
	return jsonify({'initiaized': 'initiaized'}), 201

#post /user
@app.route("/user", methods=['POST'])
def add_user():
	new_user = users(user_id = datetime.datetime.now(), name = request.json['name'], password = request.json['password'], user_id = users.get())
	new_user.save()
	return jsonify({users.select().where(users.name == request.json['name']).get(): 'initiaized'})


#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	return jsonify({'todo_get': 'todo_get'})

#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	if not request.json or not 'title' in request.json:
		abort(400)
	return jsonify({'initiaized': 'initiaized'})


#delete /todo/{id}
@app.route("/user", methods=['DELETE'])
def delete_todo():
	return jsonify({'initiaized': 'initiaized'})


#put /todo/{id}
@app.route("/user", methods=['PUT'])
def update_todo():
	return jsonify({'initiaized': 'initiaized'})


# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
