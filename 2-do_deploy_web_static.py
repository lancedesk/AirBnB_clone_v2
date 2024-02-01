#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
import os

# Define your servers' IP addresses
env.hosts = ['54.90.14.221', '204.236.240.155']
# Define the user to connect as
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive file '{archive_path}' does not exist.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the releases directory
        archive_filename = os.path.basename(archive_path)
        archive_name_no_ext = archive_filename.split('.')[0]
        releases_directory = "/data/web_static/releases/"
        release_folder = releases_directory + archive_name_no_ext + "/"
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        # Delete the uploaded archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents of release_folder/web_static/ to release_folder/
        run("mv {}web_static/* {}".format(release_folder, release_folder))
        run("rm -rf {}web_static".format(release_folder))

        # Update the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"Error: Deployment failed - {e}")
        return False
