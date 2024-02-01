#!/usr/bin/python3
"""
Fabric script that distributes an archive to my two web servers
"""

import os
from datetime import datetime
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["54.90.14.221", "204.236.240.155"]


def do_pack():
    """
    Creates a compressed archive of the web_static directory
    and stores it in the versions directory.

    Returns:
        str: Path to created archive file if successful, None otherwise.
    """
    try:
        if not os.path.isdir("versions"):
            os.makedirs("versions")

        date = datetime.now()
        zip_output = "versions/web_static_{0}{1}{2}{3}{4}{5}".format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        )
        zip_output += ".tgz"
        local("tar -cvzf {} web_static".format(zip_output))
        return zip_output

    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys the compressed archive to the web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """

    try:
        if not os.path.isfile(archive_path):
            return False

        zip_path = archive_path.split("/")[1]
        zip_name = zip_path.split(".")[0]
        put(archive_path, "/tmp/{0}".format(zip_path))

        run("sudo mkdir -p /data/web_static/releases/{}/".format(zip_name))
        src = "sudo tar -xzf /tmp/{0} -C".format(zip_path)
        dst = "/data/web_static/releases/{0}/".format(zip_name)

        run(src + " " + dst)
        run("sudo rm /tmp/{0}".format(zip_path))

        releases_dir = "/data/web_static/releases"
        src = (
            "sudo mv {}/{}/web_static/*".format(releases_dir, zip_name)
        )

        dst = "/data/web_static/releases/{0}/".format(zip_name)
        run(src + " " + dst)

        releases_2_dir = "/data/web_static/releases"
        run(
            "sudo rm -rf {}/{}/web_static".format(releases_2_dir, zip_name)
        )

        run("sudo rm -rf /data/web_static/current")
        src = "sudo ln -s /data/web_static/releases/{0}/".format(zip_name)
        dst = "/data/web_static/current"
        run(src + " " + dst)

        return True

    except Exception:
        return False
