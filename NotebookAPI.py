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
	characters.create_table()
	inventories.create_table()
	global_coords.create_table()
	weapons.create_table()
	item_effects.create_table()
	return "initialized"

@app.route("/create_user")
def create_user():
	return "created"

@app.route("/create_character")
def create_character():
	return "created"

@app.route("/move")
def move():
	return "moved"

@app.route("/buy_item")
def buy_item():
	return "bought"

@app.route("/sell_item")
def sell_item():
	return "selled"

@app.rout("/give_some_money")
def give_some_money():
	return "given"

if __name__ == "__main__":
	app.run(host='0.0.0.0')
