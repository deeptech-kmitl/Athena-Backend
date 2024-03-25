import requests
import json

url = ""

payload = json.dumps(
    {
        "cpus_per_task": 1,
        "job_name": "hello-tigerza",
        "command": "--container-image=/dataset/squashfs/nvidia+pytorch+23.01-py3.sqsh",
        "args": [
            "--no-container-mount-home",
            "--container-workdir=/root",
            "--container-remap-root",
            "--container-name=hello-tigerza",
            "--no-container-mount-home",
            "jupyter-lab",
            "--LabApp.base_url=/tiger",
            "--NotebookApp.token=bbbb",
            "--port=8989",
        ],
    }
)
headers = {
    "X-Auth-Token": "",
    "user": "",
    "Content-Type": "application/json",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
