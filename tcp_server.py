#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

"""
监听套接字负责等待有新的客户端进行连接
accept产生新的套接字用来为客户端服务
"""

def main():

    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    tcp_server_socket.bind(("",7890))

    tcp_server_socket.listen(128)

    # 循环为多个客户端服务
    while True:
        print("等待一个新的客户端的到来...")
        new_client_socket, client_addr = tcp_server_socket.accept()
        print("一个新的客户端已经到来%s " % str(client_addr))

        # 循环为同一个客户端服务多次
        while True:
            # 接受客户端发送过来的请求
            recv_data = new_client_socket.recv(1024)    #返回的只是数据
            print("客户端发送过来的请求是：%s" % recv_data.decode('utf-8'))

            # 如果recv解开堵塞，那么有两种方式：
            # 1.客户端发送过来数据
            # 2.客户端调用close导致
            if recv_data:
                new_client_socket.send("haha".encode('utf-8'))
            else:
                break
        new_client_socket.close()
        print("已经为这个客户端服务完毕")

    tcp_server_socket.close()

if __name__ == "__main__":
    main()