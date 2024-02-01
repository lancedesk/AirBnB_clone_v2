#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import put, run, env
from os.path import exists

# Servers' IP addresses
env.hosts = ['54.90.14.221', '204.236.240.155']


def do_deploy(archive_path):
    """
    Distributes an archive to the two web servers

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """

    if exists(archive_path) is False:
        return False

    try:
        zip_filename = archive_path.split("/")[-1]
        zip_no_ext = zip_filename.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        run('mkdir -p {}{}/'.format(path, zip_no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(zip_filename, path, zip_no_ext))

        # Delete the uploaded archive from the web server
        run('rm /tmp/{}'.format(zip_filename))

        # Move contents of release_folder/web_static/ to release_folder/
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, zip_no_ext))

        # Update the symbolic link /data/web_static/current
        run('rm -rf {}{}/web_static'.format(path, zip_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, zip_no_ext))

        return True

    except Exception:
        return False
