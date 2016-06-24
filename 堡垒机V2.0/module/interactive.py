"""
SSH登录模块, 引用自paramiko模块demo中的代码,
增加了命令记录数据库的功能，对于手动输入完整命令、tab补全命令、backspace删除字符修改后的命令都能完整、正确记录数据库
目前对与前后箭头位置调整还不支持
"""
import os
import paramiko
import socket
import sys
from paramiko.py3compat import u
from conf import settings
from module import common
from bll.op_log import BLL_Op_Logs

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def run(userobj, sqlhelper, ipaddr, port, sshuser, sshauth, sshkey):
    try:
        client = paramiko.SSHClient()
        #client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if sshauth == 1:
            client.connect(hostname=ipaddr, port=port, username=sshuser,password=sshkey)
        else:
            pkey = paramiko.RSAKey.from_private_key_file(os.path.join(settings.RSAKEY_PATH, sshkey))
            client.connect(hostname=ipaddr, port=port, username=sshuser, pkey=pkey)
        chan = client.invoke_shell()
        print("...正在连接.....")

        shell(userobj, sqlhelper, ipaddr, chan)

    except Exception as e:
        client.close()
        common.write_log("[module.interactive.run] {0}".format(e), "error")


def shell(userobj, sqlhelper, ipaddr, chan):
    """
    执行终端操作
    :param userobj: 当前用户对象
    :param sqlhelper: 数据库访问对象
    :param ipaddr: 当前登录的主机IP
    :param chan: 登录的终端通道
    :return:
    """
    import select
    cmd = ''
    full_cmd_list = []
    input_tab_flag = False
    op_log = BLL_Op_Logs(userobj,sqlhelper)
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if input_tab_flag:
                        cmd += x
                        input_tab_flag = False

                    if len(x) == 0:
                        # 如果用户exit退出系统,则将剩下的不够5条的记录也入库
                        if len(full_cmd_list) > 0:
                            op_log.save_log(tuple(full_cmd_list), "command")
                        #sys.stdout.write('\r\n*** EOF\r\n')
                        break

                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if ord(x) == 9:        # 用户输入tab键则记录一个标识,并不记录到命令字符中,在接收字符补全
                    input_tab_flag = True
                elif ord(x) == 127:    # 用户输入backspace键,删除一个字符
                    cmd = cmd[0:-1]
                else:
                    cmd += x.strip()


                # 如果输入回车
                if str(x) in ['\r', '\n', '\r\n']:
                    full_cmd_list.append("用户[{0}]在服务器[{1}]上执行 {2} 命令".format(userobj.username,
                                                                         ipaddr,
                                                                         cmd.strip()))
                    # 每输入5条进行一次入库
                    if len(full_cmd_list) == 5:
                        op_log.save_log(tuple(full_cmd_list), "command")
                        full_cmd_list.clear()
                    cmd = ''

                if len(x) == 0:
                    break
                chan.send(x)

    except Exception as e:
        common.write_log("[module.interactive.shell] {0}".format(e), "error")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)