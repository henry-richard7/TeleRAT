import requests


def ip_info():
    url = "http://ip-api.com/json"
    r = requests.get(url)
    data = r.json()
    return data
