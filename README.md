# ZhiHu
一个类似“知乎”的问答网站，支持注册、登录、提问、回复等功能
### 环境
* python 3.6.8
* sqlite3 3.7.17
### 搭建
* cd ZhiHu
* python -m venv my_venv
* windows
   * my_venv/Scripts/activate.bat
   * pip install -r requirements.txt
   * python manage.py runserver 0.0.0.0:8000
* linux
   * source my_venv/bin/activate
   * pip install -r requirements.txt
   * python manage.py runserver 0.0.0.0:8000
* 浏览器访问：http:://127.0.0.1:8000
(如果需要公网地址访问，记得开防火墙)
