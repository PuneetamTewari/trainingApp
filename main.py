
from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
import sqlite3
import pandas as pd


app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DEBUG"] = True
Session(app)

@app.route("/")
def index():
	session.pop('_flashes', None)
	return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")
		db_connection = sqlite3.connect('database.db')
		cursor = db_connection.cursor()
		check_credentials = """ SELECT Email, Password FROM LOGIN WHERE Password = (?); """
		result = cursor.execute(check_credentials, (password,))
		result = cursor.fetchone()
		if result is None:
			flash("Incorrect password!")
			return redirect("/login")
		else:
			find_name = """ SELECT Name FROM LOGIN WHERE Email = (?); """
			name = cursor.execute(find_name, (email,))
			name = cursor.fetchone()
			session['name'] = name
			return redirect("/profile")
		db_connection.close()
	return render_template('login.html')

@app.route('/signup', methods=["POST"])
def signup():
	if request.method == "POST":
		db_connection = sqlite3.connect('database.db')
		cursor = db_connection.cursor()
		email = request.form.get("email")
		name = request.form.get("name")
		password = request.form.get("password")
		check_credentials = """ SELECT * FROM LOGIN WHERE Email = (?); """
		result = cursor.execute(check_credentials, (email,))
		result = cursor.fetchone()
		if result is not None:
			flash("User Already Exists!!")
			return redirect("/signup")
		else:
			insertion = """ INSERT INTO LOGIN(Email, Name, Password) VALUES (?, ?, ?); """
			data = (email, name, password)
			cursor.execute(insertion, data)
			db_connection.commit()
			flash("Registered Successfully, Please login")
			return redirect("/")
		db_connection.close()
	return render_template('signup.html')

@app.route('/logout', methods=["GET"])
def logout():
	session.pop('name', None)
	return render_template('index.html')

@app.route('/profile', methods=["POST", "GET"])
def profile():
	logged_in = session['name']
	return render_template('profile.html', name=session.get('name')[0],  logged_in = logged_in)

@app.route('/createHabit', methods=["POST", "GET"])
def createHabit():
	logged_in = session['name']
	return render_template('addHabit.html', logged_in = logged_in)

@app.route('/addHabit', methods=["POST"])
def addHabit():
	if request.method == "POST":
		db_connection = sqlite3.connect('database.db')
		cursor = db_connection.cursor()
		habit = request.form.get("habit")
		check_if_exists = """ SELECT * FROM HABIT WHERE Habit = (?); """
		result = cursor.execute(check_if_exists, (habit,))
		result = cursor.fetchone()
		if result is not None:
			flash("Habit Already Exists!!")
			return redirect("/profile")
		else:
			insertion = """ INSERT INTO HABIT(Habit, Hours, Minutes) VALUES (?, ?, ?); """
			data = (habit, 0, 0)
			cursor.execute(insertion, data)
			db_connection.commit()
			flash("Habit Added Successfully!")
			return redirect("/profile")
		db_connection.close()
		logged_in = session['name']
	return render_template('profile.html', logged_in = logged_in)

@app.route('/deleteHabit', methods=["POST", "GET"])
def deleteHabit():
	logged_in = session['name']
	return render_template('deleteHabit.html', logged_in = logged_in)

@app.route('/removeHabit', methods=["POST"])
def removeHabit():
	if request.method == "POST":
		db_connection = sqlite3.connect('database.db')
		cursor = db_connection.cursor()
		habit = request.form.get("habit")
		check_if_exists = """ SELECT * FROM HABIT WHERE Habit = (?); """
		result = cursor.execute(check_if_exists, (habit,))
		result = cursor.fetchone()
		if result is None:
			flash("Habit Doesn't Exists!!")
			return redirect("/profile")
		else:
			insertion = """ DELETE FROM HABIT WHERE Habit = (?); """
			data = (habit,)
			cursor.execute(insertion, data)
			db_connection.commit()
			flash("Habit Deleted Successfully!")
			return redirect("/profile")
		db_connection.close()
		logged_in = session['name']
	return render_template('profile.html', logged_in = logged_in)

@app.route('/getHabit', methods=["POST", "GET"])
def getHabit():
	logged_in = session['name']
	db_connection = sqlite3.connect('database.db')
	cursor = db_connection.cursor()
	query = """ SELECT * FROM HABIT; """
	habitList = cursor.execute(query)
	habitList = cursor.fetchall()
	print(habitList)
	df = pd.DataFrame(data=habitList, columns=['Habit','hours','minutes'])
	html_string = df.to_html() 
	logged_in = session['name']
	return render_template('fetchHabit.html', habitList = html_string, logged_in = logged_in)

@app.route('/updateHabit', methods=["POST", "GET"])
def updateHabit():
	logged_in = session['name']
	return render_template('syncHabit.html', logged_in = logged_in)

@app.route('/syncHabit', methods=["GET", "POST"])
def syncHabit():
	if request.method == "POST":
		db_connection = sqlite3.connect('database.db')
		cursor = db_connection.cursor()
		habit = request.form.get("habit")
		hours = request.form.get("hours")
		minutes = request.form.get("minutes")
		check_if_exists = """ SELECT * FROM HABIT WHERE Habit = (?); """
		result = cursor.execute(check_if_exists, (habit,))
		result = cursor.fetchone()
		if result is None:
			flash("Habit Doesn't Exists!!")
			return redirect("/profile")
		else:
			update = """ UPDATE HABIT SET Hours = (?), Minutes = (?) WHERE Habit = (?); """
			data = (hours, minutes, habit)
			cursor.execute(update, data)
			db_connection.commit()
			flash("Habit updated successfully!")
			return redirect("/profile")
		db_connection.close()
		logged_in = session['name']
	return render_template('profile.html', logged_in = logged_in)