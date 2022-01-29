import os
import datetime
import base64

from flask import Flask, jsonify, request, make_response, send_from_directory
from werkzeug.utils import secure_filename

from dbclasses import users, todos

app = Flask(__name__)

@app.route("/")
def hello():
	hello_text = "<h1 style = 'color:green'>Default route</h1>"
	hello_text += "Routes: <br>"
	hello_text += "<li>/init_databases </li>"
	hello_text += "<li>[post] /user </li>"
	hello_text += "<li>[get] /user </li>"
	hello_text += "<li>[get] /login </li>"
	hello_text += "<li>[get] /todo </li>"
	hello_text += "<li>[post] /todo </li>"
	hello_text += "<li>[delete] /todo </li>"
	hello_text += "<li>[put] /todo </li>"
	return make_response(hello_text, 200)

#В случае существования баз данных не удаляет их, оттого сплю спокойно
@app.route("/init_databases", methods=['POST'])
def init_databases():
	users.create_table()
	todos.create_table()
	return make_response("databases initialized", 200)


#----------------------------POST/GET USER / GET LOGIN------------------------------------


#post /user
@app.route("/user", methods=['POST'])
def add_user():
	#сбор данных об окружении
	try:
		c_name = request.json['name']
		c_password = request.json['password']
	except Exception:
		return make_response("Неверные входные данные", 400)

	c_datetime = int(datetime.datetime.now().timestamp())

	#костыль для определения последнего сохранённого user_id
	user_query = users.select().dicts().execute()
	if len(user_query) == 0:
		c_id = 1
	else:
		c_id = user_query[len(user_query) - 1]['user_id'] + 1

	#c_id = len(todo_query) + ord(c_name[0]) + ord(c_password[0]) + int(c_datetime)
	b64_to_be_encoded = bytes('' + c_name + c_password + str(c_datetime), 'utf-8')
	c_session_id = str(base64.b64encode(b64_to_be_encoded))

	#основной код
	try:
		users.create(user_id = c_id, name = c_name, password = c_password, last_session_id = c_session_id)

		user = users.select().where(users.name == c_name).get()
		return make_response(jsonify({'token': user.last_session_id}), 201)
	except Exception:
		ret_text = "Произошла внутренняя ошибка сервера при попытке создания новой учётной записи"
		return make_response(ret_text, 500)


#get /user
@app.route("/user", methods=['GET'])
def get_user():
	#сбор данных об окружении
	try:
		c_session_id = request.json['token']
	except Exception:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		user = users.select().where(users.last_session_id == c_session_id).get()
		return make_response(jsonify({'name': user.name}), 200)
	except Exception:
		return make_response("Пользователь с предоставленным идентификатором сессии не был найден", 404)


#get /login
@app.route("/login", methods=['GET'])
def login():
	#сбор данных об окружении
	try:
		c_name = request.json['name']
		c_password = request.json['password']
	except Exception:
		return make_response("Неверные входные данные", 400)

	c_datetime = int(datetime.datetime.now().timestamp())
	c_session_id = str(base64.b64encode(bytes('' + c_name + c_password + str(c_datetime), 'utf-8')))

	#основной код
	try:
		user = users.get(users.name == c_name, users.password == c_password)
		user.last_session_id = c_session_id
		user.save()

		return make_response(jsonify({'token': user.last_session_id}), 200)
	except Exception:
		return make_response("Пользователь с предоставленными логином и паролем не был найден", 404)


#----------------------------POST/GET TODO-------------------------------


#post /todo
@app.route("/todo", methods=['POST'])
def add_todo():
	#Аутентификация
	try:
		c_session_id = request.json['token']
	except Exception:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == c_session_id).get()
	except Exception:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	c_user_id = user.user_id
	try:
		c_text = request.json['text']
	except Exception:
		return make_response("Неверные входные данные", 400)

	c_datetime = int(datetime.datetime.now().timestamp())
	c_todo_id = 0 + c_user_id + int(c_datetime)

	#основной код
	try:
		todos.create(todo_id = c_todo_id, user_id = c_user_id, text = c_text)

		todo = todos.select().where(todos.todo_id == c_todo_id).get()
		return make_response(jsonify({'todo_id': todo.todo_id}), 201)
	except Exception:
		return make_response("Произошла внутренняя ошибка сервера при попытке создания новой задачи", 500)


#get /todo
@app.route("/todo", methods=['GET'])
def get_todo():
	#Аутентификация
	try:
		c_session_id = request.json['token']
	except Exception:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == c_session_id).get()
	except Exception:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	c_user_id = user.user_id

	#основной код
	try:
		todo_query = todos.select().where(todos.user_id == c_user_id).dicts().execute()
		todo_output = []

		for todo in todo_query:
			todo_output.append(todo)

		return make_response(jsonify(todo_output), 200)
	except Exception:
		ret_text = "Для пользователя с предоставленным идентификатором сессии"
		ret_text += "данные о задачах не были найдены"
		return make_response(ret_text, 500)


#---------------------------DELETE/PUT TODO------------------------------


#delete /todo
@app.route("/todo", methods=['DELETE'])
def delete_todo():
	#Аутентификация
	try:
		c_session_id = request.json['token']
	except Exception:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == c_session_id).get()
	except Exception:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	c_user_id = user.user_id
	try:
		c_todo_id = request.json['todo_id']
	except Exception:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		todo = todos.get(todos.user_id == c_user_id, todos.todo_id == c_todo_id)
		todo.delete_instance()
		return make_response("Задача успешно удалена", 200)
	except Exception:
		ret_text = "Возникла внутренняя ошибка сервера при попытки удаления задачи с предоставленным"
		ret_text += " идентификатором. Возможно, задачи с таким идентификатором не существует"
		return make_response(ret_text, 500)


#put /todo
@app.route("/todo", methods=['PUT'])
def update_todo():
	#Аутентификация
	try:
		c_session_id = request.json['token']
	except Exception:
		return make_response("Неверные входные данные", 400)

	try:
		user = users.select().where(users.last_session_id == c_session_id).get()
	except Exception:
		return make_response("Пользователя с предоставленным идентификатором сессии не существует", 404)

	#сбор данных об окружении
	c_user_id = user.user_id
	try:
		c_todo_id = request.json['todo_id']
		c_text = request.json['text']
	except Exception:
		return make_response("Неверные входные данные", 400)

	#основной код
	try:
		todo = todos.get(todos.user_id == c_user_id, todos.todo_id == c_todo_id)
		todo.text = c_text
		todo.save()

		return make_response(jsonify({'todo_id': todo.todo_id}), 200)
	except Exception:
		ret_text = "Произошла внутренняя ошибка сервера при попытке обновления содержимого "
		ret_text += "задачи. Возможно, задачи с таким идентификатором не существует"
		return make_response(ret_text, 500)


#--------------------------POST/GET/DELETE FILES-----------------------------

app.config['UPLOAD_FOLDER'] = '/home/FlaskMachineUser/NotebookAPI/storage'
allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in allowed_extensions

#post /files
@app.route("/files", methods=['POST'])
def add_file():
	# Проверка на наличие файла в запросе
	if 'file' not in request.files:
		return make_response("Неверные входные данные", 400)

	file = request.files['file']

	# Отлов "пустых" файлов
	if file.filename == '':
		return make_response("Неверные входные данные", 400)

	# Если файл существует и находится в списке допустимых файлов
	if file and allowed_file(file.filename):
		# Очищаем название файла от эксплойтов пути до файла
		filename = secure_filename(file.filename)
		# Сохраняем файл на диск по пути 'main_upload_folder'
		try:
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		except Exception:
			return make_response("Странная и очень специфичная ошибка", 500)

		return make_response(str("added file:"+secure_filename(file.filename)), 200)

	return ("Странная и очень специфичная ошибка", 500)


#get /files
@app.route("/files", methods=['GET'])
def get_file():
	# Получение имени файла
	try:
		file_name = secure_filename(request.json['file_name'])
	except Exception:
		return make_response("Неверные входные данные", 400)

	# Отправка файла
	try:
		return send_from_directory(app.config["UPLOAD_FOLDER"], file_name)
	except Exception:
		return make_response("There are no such file", 404)


#delete /files
@app.route("/files", methods=['DELETE'])
def delete_file():
	# Получение имени файла
	try:
		file_name = secure_filename(request.json['file_name'])
	except Exception:
		return make_response("Неверные входные данные", 400)

	# Удаление файла
	try:
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
	except Exception:
		return make_response("There are no such file", 404)

	return make_response("deleted file:" + file_name, 200)


#-----------------------------------------------------------------


if __name__ == "__main__":
	app.run(host='1.1.1.1')
