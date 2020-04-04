# 一、邮箱开启smtp
## sina邮箱
在开启SMTP服务时会提示一个授权码，需要记录下来，之后不会再重新显示
![20200331145619](uploads/66bef759b754173b8c6929803842a966/20200331145619.jpg)

# 二、添加smtp配置
1. **编辑gitlab配置文件**
```
vim /etc/gitlab/gitlab.rb
```
修改下列配置项,此处以sina邮箱为例 <br>
```
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.sina.com"
gitlab_rails['smtp_port'] = 465 <br>
gitlab_rails['smtp_user_name'] = "XXXX@sina.com"
#此处一般为对应邮箱的授权码
gitlab_rails['smtp_password'] = "abcdefg"
gitlab_rails['smtp_domain'] = "sina.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
#smtp_port 为465，启用SSL连接，的时候才会是true，如果端口为25则不需要
gitlab_rails['smtp_tls'] = true
#此处必须与smtp_user_name和gitlab_email_from一致
user["git_user_email"] = "XXXX@sina.com"
gitlab_rails['gitlab_email_from'] = 'XXXX@sina.com'
```
更多其它邮箱配置请参考[gitlab smtp设置](https://docs.gitlab.com/omnibus/settings/smtp.html) <br>
注：163邮箱只有老的使用密码形式的邮箱才可以使用，新的使用授权码形式的邮箱如果在发邮件时不同时发给自己，会报错  <br>

2. **gitlab重新加载配置文件**
```
gitlab-ctl reconfigure
```

3. **测试发邮件**
    - 进入gitlab控制台
    ```
    gitlab-rails console
    ```
    - 查看配置
    ```
    ActionMailer::Base.delivery_method
    ActionMailer::Base.smtp_settings
    ```
    ![20200331150927](uploads/141bc4ae87d5499efd32d1196c41696a/20200331150927.jpg)

    - 测试发邮件
    ```
    Notify.test_email('XXX@sina.com','gitlab通知邮件','欢迎访问gitlab').deliver_now
    ```
    如果失败则会提示错误 <br>


# 三、配置gitlab
1. **gitlab开启邮件**
![20200331165629](uploads/39c5bbc3f7944cb01e2dbc5279770ff5/20200331165629.jpg)

2. **用户配置开启邮件**
![20200331165914](uploads/8f1adcddf4cdd09b53440766f397ebc2/20200331165914.jpg)
![20200331165440](uploads/28506e802609602f87aff42e99c8a015/20200331165440.jpg)