#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['54.90.14.221', '204.236.240.155']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives to keep.
                      0 or 1: Keep only the most recent version.
                      2: Keep the most recent and second most recent versions.
                      etc.
    """
    number = int(number)
    if number < 1:
        number = 1
    else:
        number += 1

    local_archives = local("ls -1t versions", capture=True).split("\n")
    local_count = len(local_archives)
    for i in range(number, local_count):
        local("rm -f versions/{}".format(local_archives[i]))

    remote_archives = run("ls -1t /data/web_static/releases").split("\n")
    remote_count = len(remote_archives)
    for i in range(number, remote_count):
        run("rm -rf /data/web_static/releases/{}".format(remote_archives[i]))
