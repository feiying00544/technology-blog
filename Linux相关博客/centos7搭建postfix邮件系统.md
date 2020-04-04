# 搭建DNS解析服务
1.**安装bind**

```
yum -y install bind bind-utils
```

2.**编辑named.conf**

```
vim /etc/named.conf
```

```
options {
        listen-on port 53 { 10.130.161.21; }; //监听本机IP
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        recursing-file  "/var/named/data/named.recursing";
        secroots-file   "/var/named/data/named.secroots";
        allow-query     { any; }; //允许任何人访问
```

3.**编辑区域配置**

```
vim /etc/named.rfc1912.zones
```
添加如下两项
```
//正向配置
zone "hesh.com" IN {
        type master;
        file "hesh.com.zone";
        allow-update { none; };
};
反向配置
zone "161.130.10.in-addr.arpa" IN {
        type master;
        file "hesh.com.local";
        allow-update { none; };
};
```

4.**编辑区域数据配置**
```
cd /var/named/
//注意，复制文件时必须加“-p”，表示复制过来的时候文件权限保持不变
cp -p named.localhost hesh.com.zone
cp -p named.localhost hesh.com.local
```
```
vim hesh.com.zone
```
修改最后三行
```
$TTL 1D
@       IN SOA  @ rname.invalid. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      mail.hesh.com.
        MX 10   mail.hesh.com.
mail IN A       10.130.161.21
```

```
vim hesh.com.local
```
修改第二行和最后三行
```
$TTL 1D
@       IN SOA  hesh.com rname.invalid. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      mail.hesh.com.
        MX 10   mail.hesh.com.
10      PTR     mail.hesh.com.
```
5.**修改域名服务**
```
vim /etc/resolv.conf
```
```
#添加本地IP为dns解析服务
nameserver 10.130.161.21
```
检查语法错误
```
named-checkconf 
```
6.**启动bind服务**
```
systemctl start named
systemctl enable named
```
解析验证
```
nslookup mail.hesh.com
```

# 搭建Postfix服务
1.**编辑postfix配置**
```
vim /etc/postfix/main.cf
```
```
myhostname = mail.hesh.com
mydomain = hesh.com
myorigin = $mydomain
inet_interfaces = 10.130.161.21, 127.0.0.1
mydestination = $myhostname, $mydomain, localhost
#此处必有此项，否则会无法使用收件箱
local_recipient_maps =
home_mailbox = Maildir/
```
检查语法
```
postfix check
```
重启postfix
```
systemctl restart postfix
```
2.**增加测试账号**
```
groupadd mailusers
//帐户只属于mailusers组并不能登录系统，用于测试邮件
useradd -g mailusers -s /sbin/nologin gitlab
passwd adminroot
//帐户只属于mailusers组并不能登录系统，用于测试邮件
useradd -g mailusers -s /sbin/nologin gitlabInbox
passwd admin95123
```
3.**测试发送邮件**
```
[root@SH-DEV1 named]# telnet mail.hesh.com 25
Trying 10.130.161.21...
Connected to mail.hesh.com.
Escape character is '^]'.
220 mail.hesh.com ESMTP Postfix
helo mail.hesh.com //声明本机的主机
250 mail.hesh.com
mail from:gitlab@hesh.com //声明发件人地址
250 2.1.0 Ok
rcpt to:feiying00544@163.com //声明收件人地址
250 2.1.5 Ok
data //写正文
354 End data with <CR><LF>.<CR><LF>
gitlab is work!!!
. //正文结束标记
250 2.0.0 Ok: queued as 1526B18460
quit //退出
221 2.0.0 Bye
Connection closed by foreign host.
```
查看已收到邮件 <br>
![image](uploads/fccf760234a9a69161be12eb52eafef9/image.png)