import json
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

KONG_API_URL = config["KONG_API_URL"]


def create_service(name: str, tunnel: str):
    payload = json.dumps(
        {
            "name": name,
            "url": tunnel,
        }
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request(
        "POST",
        KONG_API_URL + "/services",
        headers=headers,
        data=payload,
    )

    return response.json()


def create_route(name: str, path: str):
    payload = json.dumps({"name": name, "paths": path, "protocols": "https"})
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request(
        "POST",
        KONG_API_URL + "/services/" + name + "/routes",
        headers=headers,
        data=payload,
    )

    return response.json()


def delete_service(name: str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request(
        "DELETE",
        KONG_API_URL + "/services/" + name,
        headers=headers,
    )

    return response.json()


def delete_route(name: str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request(
        "DELETE",
        KONG_API_URL + "/services/" + name + "/routes/" + name,
        headers=headers,
    )

    return response.json()
