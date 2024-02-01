# Puppet manifest to set up web servers for deployment of web_static

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Define the Nginx configuration file content
$nginx_config_content = @(EOT)
  server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location / {
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
    }
  }
EOT

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => $nginx_config_content,
  require => Package['nginx'],
}

# Create necessary directories
file { ['/data/web_static/releases/test/', '/data/web_static/shared/']:
  ensure => directory,
}

# Create a fake HTML file with simple content
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html><head></head><body>Holberton School</body></html>',
}

# Create a symbolic link to the 'test' release
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Set ownership of the /data/ folder to the ubuntu user and group recursively
exec { 'set_ownership':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/bin:/usr/bin',
  onlyif  => 'test ! -L /data/web_static',
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
