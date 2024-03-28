import subprocess


def create_alias(name: str, local_port: int, destination: str, server: str):
    subprocess.Popen(
        "mole add alias local "
        + name
        + " \
    --source 127.0.0.1:"
        + str(local_port)
        + " \
    --destination "
        + destination
        + " \
    --server "
        + server,
        shell=True,
    )


def open_tunnel(name: str):
    # mole start alias example --detach
    subprocess.Popen(
        "mole start alias " + name + " --detach",
        shell=True,
    )


def close_tunnel(
    name: str,
):
    subprocess.Popen(
        "mole stop alias " + name + " --detach",
        shell=True,
    )


def delete_alias(
    name: str,
):
    subprocess.Popen(
        "mole delete " + name,
        shell=True,
    )
