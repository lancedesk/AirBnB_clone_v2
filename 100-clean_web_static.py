#!/usr/bin/python3
"""
Deletes out-of-date archives using the function do_clean.
"""

import os
from fabric.api import env, run, local
from datetime import datetime

# Servers' IP addresses
env.hosts = ['54.90.14.221', '204.236.240.155']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep. Default is 0.
            0 or 1: Keep only the most recent version.
            2: Keep the two most recent versions.
            etc.
    """
    number = int(number)
    if number < 1:
        number = 1

    # Local cleaning
    local_archives = sorted(os.listdir("versions"))
    for _ in range(number):
        if local_archives:
            local_archives.pop()
    with lcd("versions"):
        for archive in local_archives:
            local("rm ./{}".format(archive))

    # Remote cleaning
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [archive for archive in remote_archives
                           if "web_static_" in archive]
        for _ in range(number):
            if remote_archives:
                remote_archives.pop()
        for archive in remote_archives:
            run("rm -rf ./{}".format(archive))
