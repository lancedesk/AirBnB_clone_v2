#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns the archive path if the archive has been correctly generated,
    otherwise, it returns None
    """
    # Create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Set the name of the archive
    archive_name = "versions/web_static_" + timestamp + ".tgz"

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_name
    else:
        return None
