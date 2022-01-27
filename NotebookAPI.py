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
	return jsonify({'initiaized': 'initiaized'})

#post /user
@app.route("/user", methods=['POST'])
def add_user():
	curr_name = request.json['name']
	curr_password = request.json['password']

	users.create(user_id = int(datetime.datetime.now().timestamp()), name = curr_name, password = curr_password)

	user = users.select().where(users.name == curr_name).get()
	return jsonify({user.user_id: 'initiaized'})

#get /user
@app.route("/user", methods=['GET'])
def get_user():
	curr_name = request.json['name']
	curr_password = request.json['password']

	user = users.select().where(users.name == curr_name).get()
	return jsonify({user.user_id: 'initiaized'})


#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	return jsonify({'todo_get': 'todo_get'})

#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	curr_id = request.json['user_id']
	curr_text = request.json['text']

	user = users.select().where(users.user_id == int(curr_id)).get()
	return user

	#if (user.name != ""):
		#return jsonify({'not initiaized': 'not initiaized'})

	#todos.create(todo_id = int(datetime.datetime.now().timestamp()), user_id = curr_id, text = curr_text)


#delete /todo/{id}
@app.route("/user", methods=['DELETE'])
def delete_todo():
	todo = todos.get(user_id == request.json['user_id'], todo_id == request.json['todo_id'])
	user.delete_instance()
	return jsonify({'deleted': 'deleted'})


#put /todo/{id}
@app.route("/user", methods=['PUT'])
def update_todo():
	todo = todos(user_id == request.json['user_id'], todo_id == request.json['todo_id'])
	todo.text = request.json['user_id']
	todo.save()
	return jsonify({'added': 'added'})


# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
