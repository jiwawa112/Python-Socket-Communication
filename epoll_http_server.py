#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import select
import socket

# 单进程、单线程、非阻塞、长链接方式实现并发
# 根据用户的请求返回相应的页面
ip_addr = '127.0.0.1'
port_addr = 7890


def service_client(new_socket, request):
    """为这个客户端返回数据"""
    # 1.接受浏览器发送过来的请求，即http请求
    # GET/HTTP/1.1
    # ...
    # request = new_socket.recv(1024).decode('utf-8')
    # print(request)

    request_lines = request.splitlines()
    print("")
    print(">" * 20)
    print(request_lines)

    # GET/index.html HTTPL/1.1
    # get post put del
    file_name = ''
    ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
    if ret:
        file_name = ret.group(1)
        # print("*"*50,file_name)
        if file_name == '/':
            file_name = "/index.html"

    # 2.2准备发送给浏览器的数据---body
    # response += '<h1>haha<h1>'
    try:
        f = open('./html' + file_name, 'rb')
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += '\r\n'
        response += "-----file not find----"
        new_socket.send(response.encode('utf-8'))
    else:
        html_content = f.read()
        f.close()

        response_body = html_content
        response_header = 'HTTP/1.1 200 OK\r\n'
        response_header += 'Content-Length；%d\r\n' % len(response_body)
        response_header += '\r\n'

        response = response_header.encode('utf-8') + response_body
        new_socket.send(response.encode('utf-8'))
        new_socket.send(html_content)

    # 关闭套接字
    # new_socket.close()


def main():
    """用来完成整体的控制"""
    # 1.创建套接字
    tcp_server_sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设定套接字选项
    # 2.绑定
    tcp_server_sockt.bind(('', port_addr))
    # 3.变为监听套接字
    tcp_server_sockt.listen(128)
    tcp_server_sockt.setblocking(False)  # 将套接字变为非堵塞

    # 创建一个epoll对象
    epl = select.epoll()

    # 将监听到的套接字对应的id注册到epoll中
    epl.register(tcp_server_sockt.fileno(), select.EPOLLIN)  # tcp_server_sockt.fileno()得到套接字对应的文件描述符

    # 创建一个保存socket的字典
    fd_event_dict = dict()

    while True:
        fd_event_list = epl.poll()  # 默认堵塞，直到OS检测到数据到来,通过事件通知方式告诉程序，才会解堵塞(返回值时个列表,列表中的元素是元组)

        # [(fd,event),] 套接字对应的文件描述符，这个文件描述到底时什么事件 例如 可以调用recv接受等
        for fd, event in fd_event_list:
            # 等待新客户端的链接
            if fd == tcp_server_sockt.fileno():
                new_socket, client_addr = tcp_server_sockt.accept()
                epl.register(new_socket.fileno(), select.EPOLLIN)
                fd_event_dict[new_socket.fileno()] = new_socket
            elif event == select.EPOLLIN:
                # 判断已经链接的客户端是否有数据发送过来
                recv_data = fd_event_dict[fd].recv(1024).decode('utf-8')
                if recv_data:
                    service_client(fd_event_dict[fd], recv_data)
                else:
                    fd_event_dict[fd].close()
                    epl.unregister(fd)
                    del fd_event_dict[fd]

    # 关闭监听套接字
    tcp_server_sockt.close()


if __name__ == '__main__':
    main()