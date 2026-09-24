import json 

#Approach 1
#problem1 Invalid json
try:
    json.loads("<html> error page </html>")
except json.JSONDecodeError as e:
    print("invalid json: ", e)

#problem2

data = {"choices": []}
value = data.get("message")
print("using.get(): ", value) #none no crash

try:
    value = data["message"]
except KeyError as e:
    print("using []: crashed with", e)

#Approach 2

import json 
from typing import Any

class InvalidResponseBodyError(Exception):
    """Raised when an API response body cannot be parsed as JSON."""
    pass
def parse_body(raw_text: str) -> dict[str, Any]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise InvalidResponseBodyError(f"response body is not valid JSON: {e}") 

def get_required_field(data: dict[str, Any], key: str) -> Any:
    if key not in data:
        raise KeyError(f"Expected field {key} was missing from the response")
    return data[key]

def get_optional_field(data: dict[str, Any], key:str, default: Any= None) -> Any:
    return data.get(key, default)

if __name__ == "__main__":
    try:
        parse_body("<html> error page </html>")
    except InvalidResponseBodyError as e:
        print(f"caught it: {e}")

    payload = {"choices": []}
    optional = get_optional_field(payload, "message", default="no_message")

    print("optional field: ", optional)

    try:
        get_required_field(payload, "message")
    except KeyError as e:
        print(f"Caught it: {e}")