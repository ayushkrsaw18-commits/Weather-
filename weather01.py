import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Dashboard")
st.write("Search for any city to see its current weather and forecast.")

# -----------------------------
# API CONFIG
# -----------------------------
API_KEY = "YOUR_API_KEY"

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# -----------------------------
# CITY SEARCH
# -----------------------------
city = st.text_input(
    "🔎 Enter city name",
    placeholder="e.g. Delhi, Mumbai, London"
)

# -----------------------------
# WEATHER FUNCTION
# -----------------------------
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(CURRENT_WEATHER_URL, params=params)

    if response.status_code == 200:
        return response.json()

    return None


def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(FORECAST_URL, params=params)

    if response.status_code == 200:
        return response.json()

    return None


# -----------------------------
# MAIN APP
# -----------------------------
if city:

    with st.spinner("Fetching weather data..."):

        weather = get_weather(city)
        forecast = get_forecast(city)

    if weather is None:
        st.error("❌ City not found. Please check the spelling.")
        st.stop()

    # -------------------------
    # CURRENT WEATHER
    # -------------------------

    city_name = weather["name"]
    country = weather["sys"]["country"]

    temperature = weather["main"]["temp"]
    feels_like = weather["main"]["feels_like"]
    humidity = weather["main"]["humidity"]

    wind_speed = weather["wind"]["speed"]
    condition = weather["weather"][0]["description"]
    icon_code = weather["weather"][0]["icon"]

    sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"])
    sunset = datetime.fromtimestamp(weather["sys"]["sunset"])

    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

    st.header(f"📍 {city_name}, {country}")

    # -------------------------
    # WEATHER ICON + TEMPERATURE
    # -------------------------

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(icon_url, width=120)

    with col2:
        st.metric(
            "🌡️ Temperature",
            f"{temperature:.1f} °C"
        )

        st.write(
            f"**Condition:** {condition.title()}"
        )

    st.divider()

    # -------------------------
    # WEATHER DETAILS
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Feels Like",
            f"{feels_like:.1f} °C"
        )

    with col2:
        st.metric(
            "💧 Humidity",
            f"{humidity}%"
        )

    with col3:
        st.metric(
            "💨 Wind Speed",
            f"{wind_speed:.1f} m/s"
        )

    with col4:
        st.metric(
            "☁️ Condition",
            condition.title()
        )

    # -------------------------
    # SUNRISE / SUNSET
    # -------------------------

    st.subheader("🌅 Sun Information")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"🌄 Sunrise\n\n"
            f"{sunrise.strftime('%I:%M %p')}"
        )

    with col2:
        st.info(
            f"🌇 Sunset\n\n"
            f"{sunset.strftime('%I:%M %p')}"
        )

    # -------------------------
    # 5-DAY FORECAST
    # -------------------------

    if forecast:

        st.divider()
        st.subheader("📅 5-Day Forecast")

        daily_data = {}

        for item in forecast["list"]:

            date = item["dt_txt"].split(" ")[0]

            if date not in daily_data:
                daily_data[date] = item

        # Only first 5 days
        days = list(daily_data.items())[:5]

        cols = st.columns(len(days))

        for col, (date, data) in zip(cols, days):

            with col:

                forecast_temp = data["main"]["temp"]
                forecast_condition = data["weather"][0]["description"]

                forecast_icon = data["weather"][0]["icon"]

                forecast_icon_url = (
                    f"https://openweathermap.org/img/wn/"
                    f"{forecast_icon}@2x.png"
                )

                formatted_date = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                ).strftime("%a, %d %b")

                st.markdown(f"### {formatted_date}")

                st.image(
                    forecast_icon_url,
                    width=80
                )

                st.write(
                    f"🌡️ **{forecast_temp:.1f} °C**"
                )

                st.write(
                    f"{forecast_condition.title()}"
                )

    # -------------------------
    # TEMPERATURE GRAPH
    # -------------------------

    if forecast:

        st.divider()
        st.subheader("📈 Temperature Forecast")

        temperatures = []
        times = []

        for item in forecast["list"][:16]:

            temperatures.append(
                item["main"]["temp"]
            )

            times.append(
                datetime.strptime(
                    item["dt_txt"],
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d %b %H:%M")
            )

        chart_data = {
            "Temperature (°C)": temperatures
        }

        st.line_chart(chart_data)

        st.caption(
            "Temperature forecast for the upcoming hours."
        )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "🌦️ Weather Dashboard | Built with Python, "
    "Requests, REST API and Streamlit"
)