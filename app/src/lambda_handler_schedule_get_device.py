from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.infrastructure.data_store.device import put
from src.infrastructure.switchbot.device import get_device_status

logger = Logger()

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    device = get_device_status()
    put(device)
