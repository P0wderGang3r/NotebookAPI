from flask import Flask, jsonify, request
from peewee import *
from dbclasses import *
import datetime
import base64

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style = 'color:green'>Default route</h1>" +	"Routes: <br>" + "<li>/init_databases </li>" + "<li>[post] /user </li>" + "<li>[get] /user </li>" + "<li>[get] /login </li>" + "<li>[get] /todo </li>" + "<li>[post] /todo </li>" + "<li>[delete] /todo </li>" + "<li>[put] /todo </li>"


@app.route("/init_databases", methods=['POST'])
def init_databases():
	users.create_table()
	todos.create_table()
	return "databases initialized"


#-----------------------------------------------------------------


#post /user
@app.route("/user", methods=['POST'])
def add_user():
	#сбор данных об окружении
	curr_name = request.json['name']
	curr_password = request.json['password']

	curr_datetime = int(datetime.datetime.now().timestamp())
	user_query = users.select().dicts().execute()
	if (len(user_query) == 0):
		curr_id = 1
	else:
		curr_id = users.select().dicts().execute()[len(user_query) - 1]['user_id'] + 1

	#curr_id = len(todo_query) + ord(curr_name[0]) + ord(curr_password[0]) + int(curr_datetime)
	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	#основной код
	users.create(user_id = curr_id, name = curr_name, password = curr_password, last_session_id = curr_session_id)

	user = users.select().where(users.name == curr_name).get()
	#return jsonify({'token': user.last_session_id})
	return jsonify({'token': user.user_id})

#get /user
@app.route("/user", methods=['GET'])
def get_user():
	#сбор данных об окружении
	curr_session_id = request.json['token']

	#основной код
	user = users.select().where(users.last_session_id == curr_session_id).get()
	return jsonify({'name': user.name})

#get /login
@app.route("/login", methods=['POST'])
def login():
	#сбор данных об окружении
	curr_name = request.json['name']
	curr_password = request.json['password']

	curr_datetime = int(datetime.datetime.now().timestamp())
	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	#основной код
	user = users.get(users.name == curr_name, users.password == curr_password)
	user.last_session_id = curr_session_id
	user.save()

	return jsonify({'token': user.last_session_id})


#-----------------------------------------------------------------


#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	#Аутентификация
	curr_session_id = request.json['token']
	user = users.get()
	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return "Incorrect session identificator"

	#сбор данных об окружении
	curr_user_id = user.user_id
	curr_text = request.json['text']

	curr_datetime = int(datetime.datetime.now().timestamp())
	curr_todo_id = 0 + curr_user_id + int(curr_datetime) + ord(curr_session_id[0])

	#основной код
	try:
		todos.create(todo_id = curr_todo_id, user_id = curr_user_id, text = curr_text)

		todo = todos.select().where(todos.todo_id == curr_todo_id).get()
		return jsonify({todo.todo_id: todo.text})
	except Exception as e:
		return "There are no such user to add todo"

#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	curr_session_id = request.json['token']
	user = users.get()

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return "Incorrect session identificator"

	curr_user_id = user.user_id

	todo_query = todos.select().where(todos.user_id == curr_user_id).dicts().execute()
	todo_output = []

	for todo in todo_query:
		todo_output.append(todo)

	try:
		return jsonify(todo_output)
	except Exception as e:
		return "There are no todos for provided id in the table"


#-----------------------------------------------------------------


#delete /todo
@app.route("/todo", methods=['DELETE'])
def delete_todo():
	#Аутентификация
	curr_session_id = request.json['token']
	user = users.get()
	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return "Incorrect session identificator"

	#сбор данных об окружении
	curr_user_id = user.user_id
	curr_todo_id = request.json['todo_id']

	#основной код
	todo = todos.get(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id)
	todo.delete_instance()
	return "deleted"


#put /todo
@app.route("/todo", methods=['PUT'])
def update_todo():
	#Аутентификация
	curr_session_id = request.json['token']
	user = users.get()
	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return "Incorrect session identificator"

	#сбор данных об окружении
	curr_user_id = user.user_id
	curr_todo_id = request.json['todo_id']
	curr_text = request.json['text']

	#основной код
	todo = todos.get(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id)
	todo.text = curr_text
	todo.save()

	return jsonify({todo.todo_id: todo.text})


# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
