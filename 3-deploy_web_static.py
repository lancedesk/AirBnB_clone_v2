#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to my two web servers
"""

from fabric.api import env, local, put, run
from os.path import exists
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["54.90.14.221", "204.236.240.155"]


def do_pack():
    """
    Creates a compressed archive of the web_static directory

    Returns:
        str: Path to the created archive if successful, None otherwise.
    """
    try:
        if not exists("versions"):
            local("mkdir -p versions")

        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date_time)

        local("tar -czvf {} web_static".format(file_name))

        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys the compressed archive to the web servers

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        file_name_no_ext = file_name.split(".")[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}".format(file_name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, file_name_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(file_name_no_ext, file_name_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/current"
            .format(file_name_no_ext))
        return True
    except Exception:
        return False


def deploy():
    """
    Packs the web_static folder and deploys it to the web servers

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
