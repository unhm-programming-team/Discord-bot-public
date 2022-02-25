import requests
import json


def get_prod():
    with open('keys.txt', 'r') as file:
        lines = str(file.readline())
    key = json.loads(lines)
    return key["production"]


def get_test():
    with open('keys2.txt', 'r') as file:
        lines = str(file.readline())
    key = json.loads(lines)
    return key["testing"]
