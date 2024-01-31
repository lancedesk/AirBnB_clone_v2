#!/usr/bin/env bash
# Script to set up web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt-get -y update # Update package lists
sudo apt-get -y install nginx # Install Nginx
sudo service nginx start # Start Nginx service

default_file="/etc/nginx/sites-available/default"
# Get line number of the first occurrence of 'location' in the default Nginx config file
location=$(grep -Fn location $default_file | head -1 | cut -d":" -f1)
hbnb_static="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

# Create necessary directories if they don't exist
sudo mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"

# Create fake HTML file with simple content
echo "<h1>Hello World!</h1>" | sudo tee "/data/web_static/releases/test/index.html"
# Create symbolic link to the 'test' release
sudo ln -sf "/data/web_static/releases/test/" "/data/web_static/current"

# Give ownership of the /data/ folder to the ubuntu user and group recursively
sudo chown -hR ubuntu:ubuntu "/data/"

# Insert Nginx configuration for serving '/hbnb_static' content from the current directory
sudo sed -i "${location}i ${hbnb_static}" "${default_file}"

# Restart Nginx to apply changes
sudo service nginx restart
