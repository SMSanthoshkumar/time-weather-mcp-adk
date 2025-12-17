import datetime
import zoneinfo
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import os
from dotenv import load_dotenv
import requests

load_dotenv()


def get_weather(city: str) -> dict:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"status": "error", "error_message": "Weather API key missing"}

    url = "http://api.weatherapi.com/v1/current.json"
    params = {"q": city, "key": api_key}

    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()

    return {
        "status": "success",
        "report": (
            f"The weather in {data['location']['name']} is "
            f"{data['current']['condition']['text'].lower()} with "
            f"{data['current']['temp_c']}°C."
        )
    }


def get_current_time(city: str) -> dict:
    city_key = city.replace(" ", "_").lower()
    zones = [z for z in zoneinfo.available_timezones() if city_key in z.lower()]

    if not zones:
        return {"status": "error", "error_message": "Timezone not found"}

    tz = ZoneInfo(zones[0])
    now = datetime.datetime.now(tz)

    return {
        "status": "success",
        "report": f"Current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S')}"
    }

root_agent = Agent(
    name="location_info_agent",
    model="gemini-2.0-flash",
    description="Agent to answer time and weather queries.",
    instruction=(
        "You are a helpful assistant that answers questions about "
        "the current time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
