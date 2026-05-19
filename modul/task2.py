#!/usr/bin/python3
 
import argparse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("API_KEY")

def get_weather(city):
    params = {
       "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    res = requests.get(URL, params=params)
    return res.json()

def format_output(city, data, filter_key=None):
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = data.get("weather", [{}])[0]

    output = {
        "temperature": f"{main.get('temp')}°C",
        "feels_like": f"{main.get('feels_like')}°C",
        "humidity": f"{main.get('humidity')}%",
        "pressure": f"{main.get('pressure')} hPa",
        "wind_speed": f"{wind.get('speed')} m/s",
        "description": weather.get("description", "N/A").capitalize(),
    }

    print(f"\nCity: {city}")

    if filter_key:
        key = filter_key.lower()
        if key in output:
            print(f"{key.replace('_', ' ').title()}: {output[key]}")
        else:
            print("Invalid parameter. Available options:")
            print(", ".join(output.keys()))
    else:
        for k, v in output.items():
            print(f"{k.replace('_', ' ').title()}: {v}")



def main():
    parser = argparse.ArgumentParser(description="Weather Forecast CLI")

    parser.add_argument("-c", "--city", required=True, help="City name")
    parser.add_argument("-f", "--filter", help="Weather parameter (e.g. humidity, temperature)")

    args = parser.parse_args()

    data = get_weather(args.city)
    format_output(args.city, data, args.filter)

if __name__ == "__main__":
    main()


