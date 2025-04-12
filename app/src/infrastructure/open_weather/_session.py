import contextlib
import json

import requests
from aws_lambda_powertools import Logger

def custom_hooks(r: requests.Response, *args, **kwargs):
    try:
        logger = Logger()
        logger.info({
            "open_weather_api_request": {
                "url": r.request.url,
                "header": dict(r.request.headers),
                "body": json.dumps(r.request.body) if r.request.body is not None else None,
            },
            "open_weather_api_response": {
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
