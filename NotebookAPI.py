from flask import Flask
from peewee import *
from dbclasses import *

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style = 'color:blue'>Hello world!</h1>"

@app.route("/test")
def test_route():
	return "Test_route"

@app.route("/init_databases")
def init_databases():
	users.create_table()
	todos.create_table()
	return "initialized"

#post /user

#get /todo

#post /todo

#delete /todo/{id}

#put /todo/{id}

# Аутентификация пользователя с использованием HTTP Basic Authentication или JWT.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
