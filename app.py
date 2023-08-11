from flask import Flask, render_template, json, flash, request
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Setting Up
load_dotenv()
app = Flask(__name__)
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
app.secret_key = os.getenv("secret_key")

class Todo():
    
    def __init__(self, status="Incomplete", due_date="None", task="", notes=""):
        self.status = status
        self.due_date = due_date
        self.task = task

class TodoList(list):
    def addTodo(self, todo):
        if isinstance(todo, Todo):
            self.append(todo)
            return "Success"
        else: 
            return "Error"
first_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
two_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
three_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
four_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
five_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
six_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
seven_todo = Todo("Incomplete", "None", "Get something done...Dishes perhaps?")
my_todo_list = TodoList()
my_todo_list.addTodo(first_todo)
my_todo_list.addTodo(two_todo)
my_todo_list.addTodo(three_todo)
my_todo_list.addTodo(four_todo)
my_todo_list.addTodo(five_todo)
my_todo_list.addTodo(six_todo)
my_todo_list.addTodo(seven_todo)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/todo", methods=["GET"])
def todo():
    return render_template("todo.html", todo_list=my_todo_list)

@app.route("/weather", methods=["GET"])
def weather():
    return render_template("weather.html")

@app.route("/weather/card", methods=["GET"])
def weather_card():
    user_query = request.args.get("q")
    baseURL = "https://api.weatherapi.com/v1/current.json?key="
    query_tag = "&q="
    end = "&aqi=no"
    if user_query:
        x = requests.get(baseURL + WEATHER_API_KEY + query_tag + user_query + end)
        weatherDict = json.loads(x.content)
        timestamp = weatherDict["current"]["last_updated"]
        strp_timestamp = datetime.strptime(timestamp,"%Y-%m-%d %H:%M")
        date = strp_timestamp.strftime('%A, %B %d %Y')
        time = strp_timestamp.strftime('%I:%M%p')
    
        return render_template("weather_card.html", weatherDict=weatherDict, date=date, time=time)

@app.route("/weather/search", methods=["POST"])
def weather_search():
    baseURL = "https://api.weatherapi.com/v1/search.json?key="
    query_start = "&q="
    user_query = request.form.get("search")

    x = requests.get(baseURL + WEATHER_API_KEY + query_start + user_query)
    weatherDict = json.loads(x.content)
    return render_template("weather_search.html", weatherResults=weatherDict)

@app.route("/about", methods=["GET"])
def about():
    flash("About flash")
    return render_template("about.html")

if __name__ == "__main__":
    app.run()
