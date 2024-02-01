#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
import os.path

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

    if not os.path.isfile(archive_path):
        return False
    try:
        archive_filename = archive_path.split('/')[-1]
        archive_name_no_ext = archive_filename.split('.')[0]
        releases_dir = "/data/web_static/releases"
        path_no_ext = '{}/{}/'.format(releases_dir, archive_name_no_ext)
        symbolic_link = '/data/web_static/current'

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, path_no_ext))

        # Delete the uploaded archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents of release_folder/web_static/ to release_folder/
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))

        # Update the symbolic link /data/web_static/current
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symbolic_link))
        run('ln -s {} {}'.format(path_no_ext, symbolic_link))

        return True

    except Exception:
        return False
