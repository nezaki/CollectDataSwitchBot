from src.infrastructure.data_store._client import dynamodb_client
from src.infrastructure.switchbot.device import DeviceStatus

def put(device: DeviceStatus):
    dynamodb_client.put_item(
        TableName="DeviceStatus",
        Item={
            "DeviceID": {"S": device.device_id},
            "Time": {"S": device.time},
            "DeviceType": {"S": device.device_type},
            "Version": {"S": device.version},
            "Temperature": {"S": str(device.temperature)},
            "Battery": {"S": str(device.battery)},
            "Humidity": {"S": str(device.humidity)},
            "CO2": {"S": str(device.CO2)},
        }
    )
