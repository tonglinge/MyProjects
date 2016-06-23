#!/usr/bin/env python

import socketserver
from multiprocessing import Process
from conf import settings
from modules import server, common

class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            client_socket = self.request
            client_addr = self.client_address
            common.writelog("client {0} connected".format(client_addr), "info")
            # 发送一个成功标识
            client_socket.send(bytes("OK", encoding='utf8'))

            # 定义一个客户端用户对象
            client_user = None
            while True:
                # 从客户端获取命令信息
                recv_client_data = client_socket.recv(100)

                # 客户端退出了？
                if recv_client_data == b'':
                    common.writelog("client {0} disconnected".format(client_addr), "info")
                    client_socket.close()
                    break

                # 取命令(auth,put,get,show,cd)
                cmd = str(recv_client_data, encoding='utf-8').split("|")[0]
                common.writelog("client {0} send command {1}".format(client_addr, cmd), "info")

                # 如果是登录认证
                if cmd == "auth":
                    # 获取客户端用户对象
                    client_user = server.auth(client_socket, str(recv_client_data, 'utf-8'))
                else:
                    # 如果用户已经登录成功
                    try:
                        # 通过反射去 module/server 调用命令对应的方法
                        if hasattr(server, cmd):
                            func = getattr(server, cmd)
                            func(client_socket, client_user, str(recv_client_data, 'utf-8'))
                        else:
                            common.writelog("command {0} function not found".format(cmd), "info")

                    except Exception as e:
                        common.writelog("exec {0} error :{1}".format(cmd, e), "error")
                        client_socket.close()

        except Exception as e:
            common.writelog(e, "error")


def doprocess():
    """
    从配置文件获取ip:port，启动服务
    :return:
    """
    server_addr = (settings.FTP_SERVER_IP, settings.FTP_SERVER_PORT)
    server = socketserver.ThreadingTCPServer(server_addr, Myserver)
    server.serve_forever()

def start():
    """
    开启一个新的进程来启动FTP SERVER
    :return:
    """
    p = Process(target=doprocess, args=())
    p.start()
    return p




