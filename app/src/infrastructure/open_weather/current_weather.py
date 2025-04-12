import datetime

from pydantic import BaseModel

from src.infrastructure.open_weather._session import session
from src.infrastructure.secret.switchbot import app_id


class Weather(BaseModel):
    city_id: int
    lon: float
    lat: float
    weather: str
    temperature: float
    humidity: int
    dt: str


def get_current_weather():
    with session() as s:
        response = s.get(
            url=f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": "35.9755",
                "lon": "140.1409",
                "appid": app_id,
                "lang": "ja",
                "units": "metric",
            }
        )

    if response is None or response.status_code != 200:
        return None

    response_json = response.json()
    dt = datetime.datetime.fromtimestamp(response_json["dt"], datetime.timezone.utc)
    dt = dt.strftime('%Y/%m/%d %H:%M:%S%:z')
    return Weather(
        city_id=response_json["id"],
        lon=response_json["coord"]["lon"],
        lat=response_json["coord"]["lat"],
        weather=response_json["weather"][0]["main"],
        temperature=response_json["main"]["temp"],
        humidity=response_json["main"]["humidity"],
        dt=dt,
    )
