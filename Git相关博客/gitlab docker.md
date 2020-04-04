1.**docker拉取gitlab超慢，修改docker镜像地址**
```
vim /etc/docker/daemon.json
```
添加中科大地址
```
{
    "registry-mirrors" : ["https://docker.mirrors.ustc.edu.cn"]
}
```
重启docker
```
systemctl restart docker.service
```
2.**拉取gitlab镜像**
```
docker pull gitlab/gitlab-ce
```
3.**运行gitlab-ce镜像**
```
docker run -d  -p 8443:443 -p 8880:8880 -p 8822:22 --name gitlab-ce --restart always -v /etc/localtime:/etc/localtime -v /opt/local/docker_data/gitlab/config:/etc/gitlab -v /opt/local/docker_data/gitlab/logs:/var/log/gitlab -v /opt/local/docker_data/gitlab/data:/var/opt/gitlab gitlab/gitlab-ce
```
注:此处也可以使用docker-compose形式，附相应的ymal文件
```
version: '2'
services:
  gitlab-ce:
    image: gitlab/gitlab-ce
    restart: always
    ports:
      - "8443:443"
      - "8880:8880"
      - "8822:22"
      - "465:465"
    container_name: gitlab-ce
    volumes: 
       - /opt/docker_data/gitlab/config:/etc/gitlab
       - /opt/docker_data/gitlab/logs:/var/log/gitlab
       - /opt/docker_data/gitlab/data:/var/opt/gitlab
    environment:
      - TZ=Asia/Shanghai
```
```
docker-compose -f docker-compose.yml up -d
```
4.**由于URL访问地址是按容器的hostname来生成的，也就是容器的id，所以需要修改gitlab域名**
```
vim config/gitlab.rb
```
```
external_url 'http://10.130.161.21:8880’
gitlab_rails['gitlab_ssh_host'] = ’10.130.161.21'
#run时的端口，此处一定是对外开放的端口，否则外界无法使用ssh方式拉取代码
gitlab_rails['gitlab_shell_ssh_port'] = 8822
```
5.**重启容器**
```
Docker restart gitlab-ce
```
或者重新加载配置
```
gitlab-ctl reconfigure
```