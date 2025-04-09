import datetime

from pydantic import BaseModel, Field

from src.infrastructure.secret.switchbot import device_id
from src.infrastructure.switchbot._session import session, generate_headers


class DeviceStatus(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_type: str = Field(alias="deviceType")
    hub_device_id: str = Field(alias="hubDeviceId")
    battery: int
    version: str
    temperature: float
    humidity: int
    CO2: int
    time: str | None = None


def get_device_status():
    headers = generate_headers()
    with session() as s:
        response = s.get(
            url=f"https://api.switch-bot.com/v1.1/devices/{device_id}/status",
            headers=headers,
        )

    if response is None or response.status_code != 200:
        return None

    device = DeviceStatus(**response.json().get("body"))

    dt = datetime.datetime.fromtimestamp(int(int(headers.get("t")) / 1000), datetime.timezone.utc)
    dt = dt.strftime('%Y/%m/%d %H:%M:%S%:z')
    device.time = dt

    return device
