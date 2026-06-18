# PHP-FPM Docker Deployment

Deploy PHP-FPM with Docker and integrate with Nginx.

---

## Architecture

```mermaid
flowchart LR
    Browser[Browser] --> Nginx[Nginx<br>Port 8000]
    Nginx -->|fastcgi_pass| PHP[PHP-FPM Container<br>Port 9000]
    PHP --> Code[/var/www/html]
```

## Step 1: Pull PHP-FPM Image

```bash
docker pull php:fpm
```

## Step 2: Run with Docker Compose

```yaml
version: '2'
services:
  php-fpm:
    image: php:fpm
    restart: always
    ports:
      - 9000:9000
    volumes:
      - /opt/docker_data/php-fpm/www:/var/www
      - /opt/docker_data/php-fpm/conf:/usr/local/etc/php-fpm.d
    container_name: php-fpm
    environment:
      - TZ=Asia/Shanghai
```

```bash
docker-compose -f server_init.yaml up -d
```

## Step 3: Configure PHP-FPM Permissions

Edit `php-fpm.d/www.conf` and set the listen owner/group to match the Nginx process user:

```ini
listen.owner = nobody
listen.group = nobody
listen.mode = 0660
```

> **Note:** If `listen.owner` and `listen.group` don't match the Nginx user, you will get:
> `nginx error connect to php-fpm.sock failed (13: Permission denied)`

Restart the PHP container after changes.

## Step 4: Configure Nginx

```nginx
server {
    listen       8000;
    server_name  135.167.166.124;
    index        index.html index.htm index.php;
    root         /opt/html;

    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;

    location ~ \.php$ {
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME /var/www/html$fastcgi_script_name;
        include        fastcgi_params;
    }
}
```

> **Note:** `SCRIPT_FILENAME` must use the path inside the PHP container, not the host path.

Restart Nginx to apply changes.
