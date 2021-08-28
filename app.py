from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
import datetime
import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
PORT = os.environ.get('PORT')

app = Flask(__name__)


@app.route("/appi/get_weather_by_city", methods=["POST"])
def get_weather_by_city():
    city_name = request.get_json()["city_name"]
    lat = get_geo_location(city_name)[0]
    lon = get_geo_location(city_name)[1]
    data = get_weather_results(lat, lon, API_KEY)
    forecast = {}
    d = []

    # get weather data for current day
    current_temp = "{0:.2f}".format(data["current"]["temp"])
    feels_like = "{0:.2f}".format(data["current"]["feels_like"])
    max_temp = "{0:.2f}".format(data["daily"][0]["temp"]['max'])
    min_temp = "{0:.2f}".format(data["daily"][0]["temp"]['min'])
    current_date = datetime.datetime.fromtimestamp(data["current"]["dt"]).strftime('%Y-%m-%d')
    description = data["current"]["weather"][0]['description']
    humidity = "{0:.2f}".format(data["current"]["humidity"])
    wind = "{0:.2f}".format(data["current"]["wind_speed"])
    clouds = "{0:.2f}".format(data["current"]["clouds"])
    icon = data["current"]["weather"][0]['description']
    forecast["current_temp"] = current_temp
    forecast["feels_like"] = feels_like
    forecast["max_temp"] = max_temp
    forecast["min_temp"] = min_temp
    forecast["current_date"] = current_date
    forecast["description"] = description
    forecast["humidity"] = humidity
    forecast["wind"] = wind
    forecast["clouds"] = clouds
    forecast["icon"] = icon
    forecast_copy = forecast.copy()
    d.append(forecast_copy)

    # get weather data for the next three days
    for i in range(1, 4):
        current_temp = "{0:.2f}".format(data["daily"][i]["temp"]["day"])
        feels_like = "{0:.2f}".format(data["daily"][i]["feels_like"]["day"])
        max_temp = "{0:.2f}".format(data["daily"][i]["temp"]['max'])
        min_temp = "{0:.2f}".format(data["daily"][i]["temp"]['min'])
        current_date = datetime.datetime.fromtimestamp(data["daily"][i]['dt']).strftime('%Y-%m-%d')
        description = data["daily"][i]["weather"][0]['description']
        humidity = "{0:.2f}".format(data["daily"][i]["humidity"])
        wind = "{0:.2f}".format(data["daily"][i]["wind_speed"])
        clouds = "{0:.2f}".format(data["daily"][i]["clouds"])
        icon = data["daily"][i]["weather"][0]['icon']
        forecast["current_temp"] = current_temp
        forecast["feels_like"] = feels_like
        forecast["max_temp"] = max_temp
        forecast["min_temp"] = min_temp
        forecast["current_date"] = current_date
        forecast["description"] = description
        forecast["humidity"] = humidity
        forecast["wind"] = wind
        forecast["clouds"] = clouds
        forecast["icon"] = icon
        forecast_copy = forecast.copy()
        d.append(forecast_copy)
    return jsonify({"forecast": d})


def get_geo_location(city):
    address = city
    geolocator = Nominatim(user_agent="e_mandruy")
    location = geolocator.geocode(address)
    print(location)
    print(location.latitude, location.longitude)
    return location.latitude, location.longitude


def get_weather_results(lat, lon, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=minutely,hourly&appid={}".format(lat, lon, api_key)
    print(api_url)
    r = requests.get(api_url)
    return r.json()


@app.route("/")
def weather_dashboard():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, port=PORT, host="0.0.0.0")
