from src.infrastructure.data_store._client import dynamodb_client
from src.infrastructure.open_weather.current_weather import Weather

def put_weather(weather: Weather):
    dynamodb_client.put_item(
        TableName="Weather",
        Item={
            "CityID": {"S": str(weather.city_id)},
            "Time": {"S": weather.dt},
            "Lon": {"S": str(weather.lon)},
            "Lat": {"S": str(weather.lat)},
            "Temperature": {"S": str(weather.temperature)},
            "Humidity": {"S": str(weather.humidity)},
            "Weather": {"S": weather.weather},
        }
    )
