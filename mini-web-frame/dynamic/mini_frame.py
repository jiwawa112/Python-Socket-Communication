#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 添加数据库

import re

# url_func_dict = {
#     "/index.html":index,
#     "/conter.html":center
# }

URL_FUNC_DICT = dict()  #最终调用的是存储在字典里面的函数引用

func_list = list()
def route(url):
    def set_func(func):
        # URL_FUNC_DICT["/index.py"] = index
        URL_FUNC_DICT[url] = func
        def call_func(*args,**kwargs):
            return func(*args,**kwargs)
        return call_func
    return set_func

# 127.0.0.1:7890/index.py
@route("/index.html")
def index():
    with open("./template/index.html") as f:
        content = f.read()

    return content

# 127.0.0.1:7890/center.py
@route("/center.html")
def center():
    with open("./templates/center.html") as f:
        return f.read()

    my_stock_info = "这里是从mysql查询出来的数据..."

    content = re.sub(r"\{%content%\}",my_stock_info,content)

    return content

def application(env,start_response):
    start_response('200 OK',[('Content-Type','text/html;charset=utf-8')])

    file_name = env['PATH_INFO']
    # file_name = "/index.py"

    """
    if file_name == "/index.py":
        return index()
    elif file_name == "/center.py":
        return center()
    else:
        return "Hello World!"
    """

    try:
        # func = URL_FUNC_DICT[file_name]
        # return func()
        return URL_FUNC_DICT[file_name]
    except Exception as ret:
        return "产生了异常: %s" % str(ret)