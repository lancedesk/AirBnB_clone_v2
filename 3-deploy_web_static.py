#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to my two web servers
"""

from fabric.api import env, put, run, local
import os.path
from time import strftime

env.hosts = ['54.90.14.221', '204.236.240.155']


def do_pack():
    """
    Creates a compressed archive of the web_static directory.

    Returns:
        str: Path to the created archive if successful, None otherwise.
    """
    try:
        date_time = strftime('%Y%M%d%H%M%S')
        local('mkdir -p versions')
        file_name = 'versions/web_static_{}.tgz'.format(date_time)
        local('tar -czvf {} web_static/'.format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys the compressed archive to the web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        file_name = archive_path.split('/')[-1]
        no_ext = file_name.split('.')[0]
        path_no_ext = '/data/web_static/releases/{}/'.format(no_ext)
        symbolic_link = '/data/web_static/current'
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, path_no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symbolic_link))
        run('ln -s {} {}'.format(path_no_ext, symbolic_link))
        return True
    except Exception:
        return False


def deploy():
    """
    Packs the web_static folder and deploys it to the web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    deploy = do_deploy(archive_path)
    return deploy
