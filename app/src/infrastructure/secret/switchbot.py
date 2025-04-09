import boto3

_client = boto3.client("secretsmanager")

_secret = _client.get_secret_value(SecretId="SwitchbotApiToken")
api_token = _secret.get("SecretString")

_secret = _client.get_secret_value(SecretId="SwitchbotApiSecret")
api_secret = _secret.get("SecretString")

_secret = _client.get_secret_value(SecretId="SwitchbotDeviceID")
device_id = _secret.get("SecretString")
