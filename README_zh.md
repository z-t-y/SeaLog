# <img src="https://flog.pythonanywhere.com/static/favicon/favicon.svg" width="50px"> Flog
[英文版](./README.md)
由[Freepik]("https://www.flaticon.com/authors/freepik")制作的图标
在Flask学习期间创建的博客网站。

## 维护者

[z-t-y(Github)](https://github.com/z-t-y)
[andyzhouty(Gitee)](https://gitee.com/andyzhouty)

## 致谢

### 项目

- [Flask](https://github.com/pallets/flask)
- [Bootstrap](https://github.com/twbs/bootstrap)
- [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)
- [Flask-WTF](https://github.com/lepture/flask-wtf)

### 书籍

- [《Flask Web开发实战》](https://helloflask.com)，[李辉](https://greli.com)著
- [《Flask Web开发》](https://www.ituring.com.cn/book/2463), [Miguel Grinberg](https://blog.miguelgrinberg.com/)著，安道译

### 人员

- [李辉](https://greyli.com)

没有这些功能完备且维护良好的项目，这个网站无法成为现在的样子。同时，感谢李辉，是他的《Flask Web开发》带我走进了Flask的美好世界。

## 功能

- 登录、注册(需要邮箱验证)、登出、注销账户
- 收藏文章
- 关注用户
- 撰写文章
- 评论文章
- 消息中心
- 双语言支持 (简体中文和美式英语)

## 展望

- 聊天室
- Web API
  - Flog命令行客户端
  - Linux和Windows的Flog客户端

## 关于一些小问题

1. 为什么这个项目名为'Flog'?  
   'Flog'是Flask和Blog这两个词的组合，这个词听起来（以及看起来）像'frog'，所以我用了一只青蛙作为网站的图标。

2. 为什么这个网站有时一天有好几条提交，却有时候连续几周没有提交？  
这个网站不能及时更新因为我是一名学生（作业有点多）。

## 在本地运行这个网站

### 部署网站到本地

如果你使用pip+requirements.txt，命令如下：

```shell
git clone https://github.com/z-t-y/Flog.git ./flog # 或git clone https://gitee.com/andyzhouty/Flog.git
cd flog/
python3 -m venv venv # 如果你使用Windows,请使用 python -m venv venv
source ./venv/bin/activate # 如果你使用Windows，请使用 ./venv/Scripts/activate
pip3 install -r requirements.txt
flask run
```

如果你使用pipenv，命令如下：  
（这里的Pipfile中使用了阿里云的pypi镜像以加快国内下载速度，在国外的同学请使用传统的pip+requirements.txt）

```shell
# 克隆项目并切换到相应目录（如上）
pipenv install
pipenv shell
flask run
```

### 运行单元测试

pip+requirements.txt

```shell
# 假设已经激活了虚拟环境
pip3 install -r requirements-dev.txt
flask test
```

pipenv

```shell
pipenv install --dev
pipenv shell
pytest
```