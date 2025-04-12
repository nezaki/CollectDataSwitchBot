from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.infrastructure.data_store.device import put_device
from src.infrastructure.data_store.weather import put_weather
from src.infrastructure.open_weather.current_weather import get_current_weather
from src.infrastructure.switchbot.device import get_device_status

logger = Logger()

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    device = get_device_status()
    put_device(device)

    weather = get_current_weather()
    put_weather(weather)
