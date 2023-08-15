from flask import Flask, render_template, json, flash, request, Response
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
import lorem

# Setting Up
load_dotenv()
app = Flask(__name__)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
app.secret_key = os.getenv("secret_key")


class Todo:
    def __init__(
        self, status="Incomplete", due_date="None", task="", notes="", id=None
    ):
        self._id = id if id is not None else uuid.uuid4()
        self.status = status
        self.due_date = due_date
        self.task = task
        self.notes = notes

    @property
    def id(self):
        return str(self._id)


class TodoList(list):
    def addTodo(self, todo):
        if isinstance(todo, Todo):
            self.append(todo)
            return "Success"
        else:
            return "Error"

    def rmTodo(self, todo):
        delTodo = self.get_by_id(todo.id)
        if delTodo:
            self.remove(delTodo)
            return "Success"
        else:
            return "Error"

    def get_by_id(self, todo_id):
        for todo in self:
            if str(todo.id) == str(todo_id):
                return todo
        else:
            return None

    def update_by_id(
        self, todo_id, status="Incomplete", due_date="None", task="", notes=""
    ):
        target = self.get_by_id(todo_id)
        if target:
            target.status = status
            target.due_date = due_date
            target.task = task
            target.notes = notes
            return "Success"
        else:
            return "Error"


my_todo_list = TodoList()
i = 0
for i in range(10):
    todo = Todo("Incomplete", "None", lorem.sentence(), lorem.paragraph())
    my_todo_list.addTodo(todo)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todo/delete/<todo_id>", methods=["DELETE"])
def todoDelete(todo_id=0):
    deletedTodo = my_todo_list.get_by_id(todo_id)
    my_todo_list.rmTodo(deletedTodo)
    return Response("", "202")


@app.route("/todo", methods=["GET"])
def todo():
    return render_template("todo.html", todo_list=my_todo_list)


@app.route("/todo/<todo_id>", methods=["PUT"])
def todoUpdate(todo_id=0):
    focusTodo = my_todo_list.get_by_id(todo_id)
    result = my_todo_list.update_by_id(
        todo_id,
        request.form.get("Status") if request.form.get("Status") else "Incomplete",
        request.form.get("Due Date") if request.form.get("Due Date") else None,
        request.form.get("Task"),
        request.form.get("Notes"),
    )
    return render_template("todo_contents.html", todo=focusTodo, result=result)


@app.route("/todo/<todo_id>", methods=["GET"])
def todoGet(todo_id=0):
    focusTodo = my_todo_list.get_by_id(todo_id)
    return render_template("todo_contents.html", todo=focusTodo)


@app.route("/todo/edit/<todo_id>", methods=["GET"])
def getEditTodo(todo_id=0):
    focusTodo = my_todo_list.get_by_id(todo_id)
    return render_template("todo_contents_form.html", todo=focusTodo)


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
        strp_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        date = strp_timestamp.strftime("%A, %B %d %Y")
        time = strp_timestamp.strftime("%I:%M%p")

        return render_template(
            "weather_card.html", weatherDict=weatherDict, date=date, time=time
        )


@app.route("/weather/search", methods=["POST"])
def weather_search():
    baseURL = "https://api.weatherapi.com/v1/search.json?key="
    query_start = "&q="
    user_query = request.form.get("search")
    if user_query:
        x = requests.get(baseURL + WEATHER_API_KEY + query_start + user_query)
        weatherDict = json.loads(x.content)
        return render_template("weather_search.html", weatherResults=weatherDict)
    return ""


@app.route("/about", methods=["GET"])
def about():
    flash("About flash")
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
