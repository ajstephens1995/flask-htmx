from flask import Flask, render_template, json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Setting Up
load_dotenv()
app = Flask(__name__)
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    baseURL = "https://api.weatherapi.com/v1/current.json?key="
    queries =  "&q=Lexington KY&aqi=no"

    x = requests.get(baseURL + WEATHER_API_KEY + queries)
    weatherDict = json.loads(x.content)
    timestamp = weatherDict["current"]["last_updated"]
    strp_timestamp = datetime.strptime(timestamp,"%Y-%m-%d %H:%M")
    date = strp_timestamp.strftime('%A, %B %d %Y')
    time = strp_timestamp.strftime('%I:%M%p')

    return render_template("weather.html", weatherDict=weatherDict, date=date, time=time)

if __name__ == "__main__":
    app.run()
