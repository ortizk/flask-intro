#Import the flask module an any other needed
from flask import Flask, jsonify, render_template, redirect, request
import my_secrets
from pymongo import MongoClient


#Declare app variable and the static css file
app = Flask(__name__, static_folder = "static", static_url_path="")

#Set up Mongo database
client = MongoClient()
db = client.test_heroes # Name of new of existing database. Will create if none or access if exists
collection = db.heroes #Name of new or existing collection

#Declare the desired route's path
#Then declare a function for that route to use
# @ below is called a decorator and makes the following function be called when you call it
@app.route('/')
def home():
	return render_template('home.html', name = my_secrets.name)

# SayHi route. This has an optional param called num
@app.route('/say_hi')
@app.route('/say_hi/<num>')
def hello(num):
	return "Hello, my name is " + my_secrets.name + " and I am " + my_secrets.age + " years old"

@app.route('/hero/<name>', methods=["GET"])
def gimmeOneHero(name):
	heroes = [{'person':'Superman', 'age': 1000}, {'person':'Batman', 'age': 36}, {'person':'Thor'}, {'person':'Wonder Woman'}, {'person':'You!'}]
	# the first hero before the for in loop is what it's returning
	names = [hero for hero in heroes if hero['person'] == name]
	print(names)
	if names:
		return jsonify({'hero': names[0]})
	else:
		return "Hero not found"

@app.route('/heroes', methods=['POST'])
def create():
	person = request.form['person']
	age = request.form['age']

	new_hero = {
		'person':person,
		'age': age
	}

	db.heroes.insert_one(new_hero)
	return redirect('/')


#Similar to running app.listen on whatever port in express
#Make sure the program is listening. Default port is 5000
if __name__ == "__main__":
	app.run(debug=True)