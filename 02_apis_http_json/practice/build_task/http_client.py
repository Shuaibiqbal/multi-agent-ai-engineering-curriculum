import requests
import random
from exceptions import TransientHTTPError, PermanentHTTPError
from logging_setup import logging_setup
import time
import json


logger = logging_setup(__name__)

def compute_bakoff(attempt: int) -> float:

    return 2 ** attempt + random.uniform(0, 1)


def request_with_retry(method: str, url:str, max_attempts: int = 5, **kwargs) -> dict:

    for attempt in range(max_attempts):
        logger.debug(f"attempt {attempt}: {method} {url}")

        try:
            response = requests.request(method, url, timeout=(3,10), **kwargs)
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError) as e:
            if attempt == max_attempts -1:
                logger.error(
                    f"gave up after {max_attempts} attempts {e}"
                             )
                raise TransientHTTPError(str(e))
            time.sleep(compute_bakoff(attempt=attempt))
            continue
        if response.status_code < 300:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise TransientHTTPError(f"bad JSON in response {e}")   
        if response.status_code == 429 or response.status_code // 100 == 5:
            if attempt == max_attempts - 1:
                logger.error(f"gave up, last status {response.status_code}")
                raise TransientHTTPError(f"status {response.status_code}")
            time.sleep(compute_bakoff(attempt))
            continue
        logger.error(f"Permanent failure: status {response.status_code}")
        raise PermanentHTTPError(response.status_code, response.text)

if __name__ == "__main__":
    print(request_with_retry("GET", "https://api.github.com"))