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
	users.create(user_id = int(datetime.datetime.now().timestamp()), name = request.json['name'], password = request.json['password'])
	return jsonify({users.get(name == str(request.json['name'])).name: 'initiaized'})


#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	return jsonify({'todo_get': 'todo_get'})

#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	if (users.get(user_id == int(request.json['user_id'])).name != ""):
		todos.create(user_id == int(request.json['user_id']), todo_id = 0, date = datetime.datetime.now(), text = request.json['text'])
		return jsonify({'initiaized': 'initiaized'})
	return jsonify({'not initiaized': 'not initiaized'})


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
