import json
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

KONG_API_URL = config["KONG_API_URL"]
LAB_DOMAIN = config["LAB_DOMAIN"]


def create_service(name: str, port: int, path: str):
    payload = json.dumps(
        {
            "name": name,
            "host": "127.0.0.1",
            "port": port,
            "protocol": "http",
            "path": path,
        }
    )
    print(payload, path)
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST",
        KONG_API_URL + "/services",
        headers=headers,
        data=payload,
    )

    print(response)

    return response.json()


def create_route(name: str, path: str):
    payload = json.dumps(
        {
            "name": name,
            "paths": [path],
            "protocols": ["https"],
            "hosts": [LAB_DOMAIN],
            "preserve_host": True,
        }
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST",
        KONG_API_URL + "/services/" + name + "/routes",
        headers=headers,
        data=payload,
    )

    print(response)

    return response.json()


def delete_service(name: str):
    headers = {
        "Content-Type": "application/json",
    }

    requests.request(
        "DELETE",
        KONG_API_URL + "/services/" + name,
        headers=headers,
    )


def delete_route(name: str):
    headers = {
        "Content-Type": "application/json",
    }

    requests.request(
        "DELETE",
        KONG_API_URL + "/services/" + name + "/routes/" + name,
        headers=headers,
    )
