#!/usr/bin/python3
"""
Deletes out-of-date archives using the function do_clean.
"""

import os
from fabric.api import *

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
    number = 1 if int(number) == 0 else int(number)

    # Local cleaning
    zips = sorted(os.listdir("versions"))
    [zips.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in zips]

    # Remote cleaning
    with cd("/data/web_static/releases"):
        zips = run("ls -tr").split()
        zips = [a for a in zips if "web_static_" in a]
        [zips.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in zips]
