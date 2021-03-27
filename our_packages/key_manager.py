import requests


def get_prod():
    response = requests.get("http://34.68.101.38:5005/production")
    return response.content.decode("utf-8")


def get_test():
    response = requests.get("http://34.68.101.38:5005/testing")
    return response.content.decode("utf-8")
