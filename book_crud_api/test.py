import requests

if __name__ == '__main__':
    requests.post(url="http://localhost:8080/", json={
        "name": "Artem",
        "count": 10
    })