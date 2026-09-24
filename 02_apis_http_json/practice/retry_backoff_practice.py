import requests
import time 

# url = "http://10.255.255.1"

# max_attempts = 5
# response = None

# for attempt in range(max_attempts):
#     try:
#         response = requests.get(url, timeout=(3, 5))
#         break
#     except requests.exceptions.Timeout:
#         print("attempt", attempt, "timed out")
#         print(f"Time Now: {time.gmtime().tm_hour}:{time.gmtime().tm_min}:{time.gmtime().tm_sec}")
#         if attempt == max_attempts -1:
#             print("gave up after", max_attempts, "attempts")
#         else:
#             time.sleep(2** attempt)
# if response is not None:
#     print(response.status_code)
#Version2

import logging

logger = logging.getLogger(__name__)

def get_with_retry(url: str, max_attempts: int = 5) -> requests.Response:
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=(3,5))
        except requests.exceptions.Timeout:
            if attempt == max_attempts -1:
                logging.error(f"{max_attempts} times attempted but got no response")
            wait_seconds = 2 ** attempt

            logging.warning(
                "attempt %s timed out, waiting %ss", attempt, wait_seconds
            )
            time.sleep(wait_seconds)
            # raise RuntimeError("unreachable") # uncomment in production level

if __name__ == "__main__":
    url = "http://10.255.255.1"
    get_with_retry(url=url)


## 429 status-code handling
response = {"status_code": 429,
             "headers": {"Retry-After": "2"}}
class FakeResponse:
    def __init__(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers
def decides_wait_seconds(response, attempt):
    retry_after = response.headers.get("Retry-After")
    if retry_after is not None:
        return int(retry_after)
    return 2 ** attempt
# test: server told us how long to wait
r1 = FakeResponse(response["status_code"], response["headers"])
print(decides_wait_seconds(r1, attempt=0))
# test: server didn't say, fall back to backoff
r2 = FakeResponse(response['status_code'], {})
print(decides_wait_seconds(r2, attempt=3))