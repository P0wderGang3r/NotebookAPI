from flask import Flask
from peewee import *
from dbclasses import *

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style = 'color:green'>Default route</h1>" +	"Routes: <br>" + "<li>/init_databases </li>" + "<li>[post] /user </li>" + "<li>[get] /todo </li>" +	"<li>[post] /todo </li>" + "<li>[delete] /todo/{id} </li>" + "<li>[put] /todo/{id} </li>"

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
