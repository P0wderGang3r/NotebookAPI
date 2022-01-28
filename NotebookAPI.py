from flask import Flask, jsonify, request, make_response
from peewee import *
from dbclasses import *
import datetime
import base64

app = Flask(__name__)

@app.route("/")
def hello():
	return make_response("<h1 style = 'color:green'>Default route</h1>" +	"Routes: <br>" + "<li>/init_databases </li>" + "<li>[post] /user </li>" + "<li>[get] /user </li>" + "<li>[get] /login </li>" + "<li>[get] /todo </li>" + "<li>[post] /todo </li>" + "<li>[delete] /todo </li>" + "<li>[put] /todo </li>", 200)

#В случае существования баз данных не удаляет их, оттого сплю спокойно
@app.route("/init_databases", methods=['POST'])
def init_databases():
	users.create_table()
	todos.create_table()
	return make_response("databases initialized", 200)


#-----------------------------------------------------------------


#post /user
@app.route("/user", methods=['POST'])
def add_user():
	#сбор данных об окружении
	try:
		curr_name = request.json['name']
		curr_password = request.json['password']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	curr_datetime = int(datetime.datetime.now().timestamp())

	#костыль для определения последнего сохранённого user_id
	user_query = users.select().dicts().execute()
	if (len(user_query) == 0):
		curr_id = 1
	else:
		curr_id = user_query[len(user_query) - 1]['user_id'] + 1

	#curr_id = len(todo_query) + ord(curr_name[0]) + ord(curr_password[0]) + int(curr_datetime)
	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	#основной код
	try:
		users.create(user_id = curr_id, name = curr_name, password = curr_password, last_session_id = curr_session_id)

		user = users.select().where(users.name == curr_name).get()
		return make_response(jsonify({'token': user.last_session_id}), 201)
	except Exception as e:
		return make_response("Произошла внутренняя ошибка сервера при попытке создания новой учётной записи", 500)


#get /user
@app.route("/user", methods=['GET'])
def get_user():
	#сбор данных об окружении
	try:
		curr_session_id = request.json['token']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
		return make_response(jsonify({'name': user.name}), 200)
	except Exception as e:
		return make_response("Пользователь с предоставленным идентификатором сессии не был найден", 404)

#get /login
@app.route("/login", methods=['GET'])
def login():
	#сбор данных об окружении
	try:
		curr_name = request.json['name']
		curr_password = request.json['password']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	curr_datetime = int(datetime.datetime.now().timestamp())
	curr_session_id = str(base64.b64encode(bytes('' + curr_name + curr_password + str(curr_datetime), 'utf-8')))

	#основной код
	try:
		user = users.get(users.name == curr_name, users.password == curr_password)
		user.last_session_id = curr_session_id
		user.save()

		return make_response(jsonify({'token': user.last_session_id}), 200)
	except Exception as e:
		return make_response("Пользователь с предоставленными логином и паролем не был найден", 404)


#-----------------------------------------------------------------


#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	#Аутентификация
	try:
		curr_session_id = request.json['token']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	curr_user_id = user.user_id
	try:
		curr_text = request.json['text']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	curr_datetime = int(datetime.datetime.now().timestamp())
	curr_todo_id = 0 + curr_user_id + int(curr_datetime)

	#основной код
	try:
		todos.create(todo_id = curr_todo_id, user_id = curr_user_id, text = curr_text)

		todo = todos.select().where(todos.todo_id == curr_todo_id).get()
		return make_response(jsonify({todo.todo_id: todo.text}), 201)
	except Exception as e:
		return make_response("Произошла внутренняя ошибка сервера при попытке создания новой задачи", 500)

#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	#Аутентификация
	try:
		curr_session_id = request.json['token']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	curr_user_id = user.user_id

	#основной код
	try:
		todo_query = todos.select().where(todos.user_id == curr_user_id).dicts().execute()
		todo_output = []

		for todo in todo_query:
			todo_output.append(todo)

		return make_response(jsonify(todo_output), 200)
	except Exception as e:
		return make_response("Для пользователя с предоставленным идентификатором сессии данные о задачах не были найдены", 500)


#-----------------------------------------------------------------


#delete /todo
@app.route("/todo", methods=['DELETE'])
def delete_todo():
	#Аутентификация
	try:
		curr_session_id = request.json['token']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	curr_user_id = user.user_id
	try:
		curr_todo_id = request.json['todo_id']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		todo = todos.get(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id)
		todo.delete_instance()
		return make_response("Задача успешно удалена", 200)
	except Exception as e:
		return make_response("Возникла внутренняя ошибка сервера при попытки удаления задачи с предоставленным идентификатором. Возможно, задачи с таким идентификатором не существует", 500)



#put /todo
@app.route("/todo", methods=['PUT'])
def update_todo():
	#Аутентификация
	try:
		curr_session_id = request.json['token']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == curr_session_id).get()
	except Exception as e:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	curr_user_id = user.user_id
	try:
		curr_todo_id = request.json['todo_id']
		curr_text = request.json['text']
	except Exception as e:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		todo = todos.get(todos.user_id == curr_user_id, todos.todo_id == curr_todo_id)
		todo.text = curr_text
		todo.save()

		return make_response(jsonify({todo.todo_id: todo.text}), 200)
	except Exception as e:
		return make_response("Произошла внутренняя ошибка сервера при попытке обновления содержимого задачи. Возможно, задачи с таким идентификатором не существует", 500)


#-----------------------------------------------------------------


if __name__ == "__main__":
	app.run(host='0.0.0.0')
