import requests


#version1

session = requests.session()
# session.auth = ("user", "pass") # overwrite actual toke or pass actual token
session.headers.update({"Authorization": "fake-token"})

urls = [
 "https://api.github.com",
 "https://api.github.com/zen",
 "https://api.github.com/octocat",
]

for url in urls:
    response = session.get(url=url)
    print(url, "->", response.status_code)

print("Autorization header set to: ", response.request.headers["Authorization"])

##Version2

def make_authenticated_session(token: str) -> requests.Session:

    session1 = requests.Session()

    session1.headers.update({"Authorization": f"{token}"})

    return session1

def main() -> None:
    session1 = make_authenticated_session("fake-token")

    urls = [
            "https://api.github.com",
            "https://api.github.com/zen",
            "https://api.github.com/octocat",
            ]
    for url in urls:
        response = session1.get(url)

        print(f"{url} -> {response.status_code}")
    print(f"header actually sent on the last request: {response.request.headers.get("Authorization")}")

if __name__ == "__main__":
    main()