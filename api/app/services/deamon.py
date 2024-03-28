import os
import subprocess


template = """[Service]
Environment = "P1=start" "P2=alias" "P3={id}"
ExecStart=/usr/local/bin/mole $P1 $P2 $P3
Restart=always
RestartSec=10
StandardOutput = file:/tmp/service-{id}.log
User=root"""


def activate_service(id: str):
    f = open(
        "/etc/systemd/system/" + id + ".service",
        "a",
    )
    f.write(template.replace("{id}", id))
    f.close()
    subprocess.Popen(
        "systemctl daemon-reload",
        shell=True,
    )
    subprocess.Popen(
        "systemctl enable " + id,
        shell=True,
    )
    subprocess.Popen(
        "systemctl start " + id,
        shell=True,
    )


def deactivate_service(id: str):
    subprocess.Popen(
        "systemctl disable " + id,
        shell=True,
    )
    subprocess.Popen(
        "systemctl stop " + id,
        shell=True,
    )
    os.remove("/etc/systemd/system/" + id + ".service")
    subprocess.Popen(
        "systemctl daemon-reload",
        shell=True,
    )
