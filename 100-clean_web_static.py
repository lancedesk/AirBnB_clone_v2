#!/usr/bin/python3
"""
Fabric script for managing deployment % cleanup of web server archives.
"""

from fabric.api import env, put, run, local
import os.path
from time import strftime

# Servers' IP addresses
env.hosts = ['54.90.14.221', '204.236.240.155']


def do_pack():
    """
    Create a compressed archive of the web_static directory.

    Returns:
        str: Path to created archive if successful, None otherwise.
    """
    try:
        curr_time = strftime('%Y%M%d%H%M%S')
        local('mkdir -p versions')
        zip_name = 'versions/web_static_{}.tgz'.format(curr_time)
        local('tar -czvf {} web_static/'.format(zip_name))
        return zip_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy the compressed archive to the web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        zip_name = archive_path.split('/')[-1]
        no_ext = zip_name.split('.')[0]
        path_no_ext = '/data/web_static/releases/{}/'.format(no_ext)
        symbolic_link = '/data/web_static/current'
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(zip_name, path_no_ext))
        run('rm /tmp/{}'.format(zip_name))
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symbolic_link))
        run('ln -s {} {}'.format(path_no_ext, symbolic_link))
        return True
    except Exception:
        return False


def deploy():
    """
    Pack the web_static folder and deploy it to the web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    zip_path = do_pack()
    if zip_path is None:
        return False
    deploy = do_deploy(zip_path)
    return deploy


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep. Default is 0.
            0 or 1: Keep only the most recent version.
            2: Keep the two most recent versions.
            etc.
    """
    local_ = 'versions/*.tgz'
    run_ = '/data/web_static/releases/web_static*'
    if number == 0:
        number = 1
    local("rm -f `ls -t {} | awk 'NR>{}'`".format(local_, number))
    run("rm -rf `ls -td {} | awk 'NR>{}'`".format(run_, number))
