import requests

url = "https://api.github.com"

response = requests.get(url)

print(response.status_code)
print(response.json())
print(response.json().keys())

## Invalid Url 
print("Invalid Url test")
url2 = "htp://api.github.com"
try:
    response2 = requests.get(url2)

    print(response2.status_code)
except Exception as e:
    print(type(e).__name__)

### Version2

def main() -> None:
    url_v2 = "https://api.github.com"
    response = requests.get(url_v2)
    print(f"Status: {response.status_code}")
    print(f"body: {response.json()}")
    try:
        url_v2 = "htps://api.github.com"
        response_v3 = requests.get(url_v2)
    except requests.exceptions.RequestException as e:
        print(f"Caught a client-side request error {type(e).__name__} - {e}")
if __name__ == "__main__":
    main()