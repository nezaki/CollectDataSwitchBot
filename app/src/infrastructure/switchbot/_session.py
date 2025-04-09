import base64
import contextlib
import hashlib
import hmac
import json
import time
import uuid

import requests
from aws_lambda_powertools import Logger

from src.infrastructure.secret.switchbot import api_token, api_secret

def custom_hooks(r: requests.Response, *args, **kwargs):
    try:
        logger = Logger()
        logger.info({
            "switchbot_api_request": {
                "url": r.request.url,
                "header": dict(r.request.headers),
                "body": json.dumps(r.request.body) if r.request.body is not None else None,
            },
            "switchbot_api_response": {
                "status_code": r.status_code,
                "header": dict(r.headers),
                "body": r.json(),
            }
        })
    except:
        pass
    return r

@contextlib.contextmanager
def session():
    _session = requests.Session()
    _session.hooks["response"] = [custom_hooks]
    try:
        yield _session
    finally:
        _session.close()

def generate_headers():
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = bytes(f"{api_token}{t}{nonce}", "utf-8")
    sign = base64.b64encode(
        hmac.new(key=bytes(api_secret, "utf-8"), msg=string_to_sign, digestmod=hashlib.sha256).digest()
    )
    sign = str(sign, "utf-8")
    return {
        "Authorization": api_token,
        "sign": sign,
        "t": str(t),
        "nonce": str(nonce),
    }
