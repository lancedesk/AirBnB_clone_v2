#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['54.90.14.221', '204.236.240.155']


def do_deploy(archive_path):
    """
    Creates a compressed archive of the web_static directory,
    packs it with a timestamp, and stores it in the versions directory.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        str: The path to created archive file if successful, None otherwise.
    """

    if not os.path.isdir("versions"):
        os.mkdir("versions")
    current_time = datetime.now()

    zip_output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )

    try:
        print("Packing web_static to {}".format(zip_output))
        local("tar -cvzf {} web_static".format(zip_output))
        zip_size = os.stat(zip_output).st_size
        print("web_static packed: {} -> {} Bytes".format(zip_output, zip_size))

    except Exception:
        zip_output = None

    return zip_output


def do_deploy(archive_path):
    """
    Deploys the compressed archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """

    if not os.path.exists(archive_path):
        return False

    zip_name = os.path.basename(archive_path)
    dir_name = zip_name.replace(".tgz", "")
    dir_path = "/data/web_static/releases/{}/".format(dir_name)

    success = False
    try:
        put(archive_path, "/tmp/{}".format(zip_name))
        run("mkdir -p {}".format(dir_path))
        run("tar -xzf /tmp/{} -C {}".format(zip_name, dir_path))
        run("rm -rf /tmp/{}".format(zip_name))
        run("mv {}web_static/* {}".format(dir_path, dir_path))
        run("rm -rf {}web_static".format(dir_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dir_path))
        print('New version deployed!')
        success = True

    except Exception:
        success = False

    return success
