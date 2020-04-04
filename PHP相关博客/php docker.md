1.**拉取php-fpm镜像**
```
docker pull php:fpm
```
2.**使用docker compose运行php-fpm**
```
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
```
docker-compose -f server_init.yaml up -d
```
3.**修改php配置**
配置位于php-fpm.d的www.conf，之后重启php容器
```
listen.owner = nobody
listen.group = nobody
listen.mode = 0660
将原listen.owner，listen.group段做如上修改，其中listen.owner，listen.group为nginx启动用户名，如此处不修改，会提示
nginx error connect to php-fpm.sock failed (13: Permission denied)
```
4.修改nginx配置
```
server {
        listen          8000;
        server_name     135.167.166.124;
        index           index.html index.htm index.php;
        root            /opt/html;#代码在宿主路径

        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;

        location ~ \.php$ {
           fastcgi_pass    127.0.0.1:9000;
           fastcgi_index   index.php;
           fastcgi_param   SCRIPT_FILENAME  /var/www/html$fastcgi_script_name;#此处路径为php容器内放置代码路径
           include         fastcgi_params;
        }

    }
```
重启nginx即可