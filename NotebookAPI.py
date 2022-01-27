from flask import Flask, jsonify, request
from peewee import *
from dbclasses import *
import datetime
import base64

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

#-----------------------------------------------------------------
#Нужна генерация новых токенов входа

#post /user
@app.route("/user", methods=['POST'])
def add_user():
	curr_name = request.json['name']
	curr_password = request.json['password']
	curr_datetime = int(datetime.datetime.now().timestamp())


	curr_id = 0 + ord(curr_name[0]) + ord(curr_password[0]) + int(curr_datetime)
	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	users.create(user_id = curr_id, name = curr_name, password = curr_password, last_session_id = curr_session_id)

	user = users.select().where(users.name == curr_name).get()
	return jsonify({'token': user.last_session_id})

#get /user
@app.route("/user", methods=['GET'])
def get_user():
	curr_session_id = request.json['token']

	user = users.select().where(users.last_session_id == curr_session_id).get()
	return jsonify({'name': user.name})

#get /login
@app.route("/login", methods=['POST'])
def login():
	curr_name = request.json['name']
	curr_password = request.json['password']
	curr_datetime = int(datetime.datetime.now().timestamp())

	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	user = users.get(users.name == curr_name, users.password == curr_password)
	user.last_session_id = curr_session_id
	user.save()

	return jsonify({'token': user.last_session_id})

#-----------------------------------------------------------------

#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	curr_session_id = request.json['token']
	user = users.get()

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return "Incorrect session identificator"

	curr_user_id = user.user_id
	curr_text = request.json['text']
	curr_datetime = int(datetime.datetime.now().timestamp())

	curr_todo_id = 0 + curr_user_id + int(curr_datetime) + ord(curr_session_id[0])

	try:
		todos.create(todo_id = curr_todo_id, user_id = curr_user_id, text = curr_text)

		todo = todos.select().where(todos.user_id == curr_user_id).get()
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

	todo_query = todos.get(todos.user_id == curr_user_id)
	todo_output = []

	for todo in todo_query:
		todo_output.append(sonify(todo.todo_id, todo.text))

	#try:
	return jsonify(todo_output)
	#except Exception as e:
		#return "There are no todos for provided id in the table"

#-----------------------------------------------------------------

#delete /todo/{id}
@app.route("/user", methods=['DELETE'])
def delete_todo():
	curr_user_id = request.json['user_id']
	curr_todo_id = request.json['todo_id']

	todo = todos.get(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id)
	todo.delete_instance()
	return "deleted"


#put /todo/{id}
@app.route("/user", methods=['PUT'])
def update_todo():
	curr_user_id = request.json['user_id']
	curr_todo_id = request.json['todo_id']
	curr_text = request.json['text']

	todo = todos.select().where(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id).get()
	todo.text = curr_text
	todo.save()

	return jsonify({'added': 'added'})


# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
