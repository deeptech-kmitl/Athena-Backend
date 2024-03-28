import requests
import json

from models.image import Image
from models.instance import Instance
from models.package import Package
from models.slurmer_cluster import SlurmerCluster


def submit_job(
    slurmer: SlurmerCluster, instance: Instance, image: Image, package: Package
):
    payload = json.dumps(
        {
            "cpus_per_task": 1,
            "job_name": "athena-" + instance.tunnel_id,
            "command": "--container-image=" + image.squashfs_location,
            "args": [
                "--no-container-mount-home",
                "--container-workdir=/root",
                "--container-remap-root",
                "--container-name=" + instance.tunnel_id,
                "--no-container-mount-home",
                "jupyter-lab",
                "--LabApp.base_url=/lab/" + instance.tunnel_id,
                "--NotebookApp.token=" + instance.token,
                "--port=" + str(instance.remote_port),
            ],
        }
    )
    headers = {
        "X-Auth-Token": slurmer.token,
        "user": slurmer.user,
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST",
        slurmer.url + "/apps/" + slurmer.app_id + "/jobs",
        headers=headers,
        data=payload,
    )

    return response.json()


def get_job_status(slurmer: SlurmerCluster, instance: Instance):
    headers = {
        "X-Auth-Token": slurmer.token,
        "user": slurmer.user,
        "Content-Type": "application/json",
    }

    response = requests.request(
        "GET",
        slurmer.url + "/apps/" + slurmer.app_id + "/jobs/" + instance.job_id,
        headers=headers,
    )

    return response.json()


def start_job(slurmer: SlurmerCluster, job_id: str):
    headers = {
        "X-Auth-Token": slurmer.token,
        "user": slurmer.user,
        "Content-Type": "application/json",
    }

    requests.request(
        "PUT",
        slurmer.url + "/apps/" + slurmer.app_id + "/jobs/" + job_id + "/start",
        headers=headers,
    )


def stop_job(slurmer: SlurmerCluster, job_id: str):
    headers = {
        "X-Auth-Token": slurmer.token,
        "user": slurmer.user,
        "Content-Type": "application/json",
    }

    requests.request(
        "PUT",
        slurmer.url + "/apps/" + slurmer.app_id + "/jobs/" + job_id + "/stop",
        headers=headers,
    )


def delete_job(slurmer: SlurmerCluster, job_id: str):
    headers = {
        "X-Auth-Token": slurmer.token,
        "user": slurmer.user,
        "Content-Type": "application/json",
    }

    requests.request(
        "DELETE",
        slurmer.url + "/apps/" + slurmer.app_id + "/jobs/" + job_id,
        headers=headers,
    )
