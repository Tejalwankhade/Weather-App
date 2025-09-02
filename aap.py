import streamlit as st
import requests
from datetime import datetime


API_KEY = "f294ea74a0eecb7fd8e6555024bfd695"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Weather App", page_icon="⛅", layout="centered")

st.title("🌦️ Real-Time Weather App")
st.write("Get real-time weather details for any city in the world!")

city = st.text_input("Enter City Name", "Mumbai")

if st.button("Get Weather"):
    if city.strip():
        params = {
            "q": city.strip(),
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            st.write(f"🔍 Debug URL: {response.url}")  # Debugging line
            response.raise_for_status()
            data = response.json()

            if data.get("cod") == 200:
                # Extract Data
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                weather_desc = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                country = data["sys"]["country"]
                sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
                sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

                # Display Weather Data
                st.success(f"Weather in {city.title()}, {country}")
                st.metric("Temperature 🌡️", f"{temp}°C", f"Feels like {feels_like}°C")
                st.write(f"**Condition:** {weather_desc}")
                st.write(f"**Humidity:** {humidity}%")
                st.write(f"**Wind Speed:** {wind_speed} m/s")
                st.write(f"**Sunrise:** {sunrise} | **Sunset:** {sunset}")
            else:
                st.error(f"❌ City '{city}' not found! Try checking the spelling.")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Error connecting to API: {e}")
    else:
        st.warning("Please enter a city name.")

st.caption("Powered by [OpenWeatherMap](https://openweathermap.org/) API")
