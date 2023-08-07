from flask import Flask, render_template, json
import config
import requests
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    baseURL = "https://api.weatherapi.com/v1/current.json?key="
    queries =  "&q=Lexington KY&aqi=no"
    x = requests.get(baseURL + config.WEATHER_API_KEY + queries)
    weatherDict = json.loads(x.content)
    timestamp = weatherDict["current"]["last_updated_epoch"]
    date = datetime.fromtimestamp(timestamp).strftime('%A, %B %d %Y')
    time = datetime.fromtimestamp(timestamp).strftime('%I:%M%p')

    return render_template("weather.html", weatherDict=weatherDict, date=date, time=time)

if __name__ == "__main__":
    app.run()
