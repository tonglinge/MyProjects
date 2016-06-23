简单版堡垒机 
__author: wangsong
blog: blog.csdn.net/songfreeman

一、运行说明：
本程序使用python3开发，在 ubuntu 系统下调试通过，运行方法： python3 main.py

二、功能说明:
  本程序是一个简单版本的堡垒机程序,主要功能包括如下：
  1 实现用户认证登录
  2 对主机进行分组，一个用户可以管理不同主机组
  3 支持对单个主机执行命令、上传文件、下载文件
  4 支持对一个组的机器进行批量执行命令、上传文件
  5 通过命令查看当前用户管理的组及组内的服务器信息
  6 记录用户操作日志

三、用到主要知识点
1 模块 paramiko的使用
2 xml文件的创建、读取操作
3 进程池 multiprocessing.Pool

四、程序目录说明
.
├── main.py                   主程序模块
├── conf                      配置文件目录
│   └── settings.py           配置文件
├── dbhelper                  数据访问层
│   ├── dbapi.py              数据访问接口模块 ( 对数据库表xml文件进行信息读取接口 )
├── dbstore                   数据库目录
│   ├── groups.xml            服务器组表
│   ├── hosts.xml             服务器资源表
│   ├── init_db.py            数据初始化模块
│   └── users.xml             用户信息表
├── logs                     日志目录
│   ├── syslog.log            系统日志
│   ├── oplog.log             操作日志
├── modules                  模块文件目录
│   ├── commands.py           命令处理模块  ( 用来分析用户命令、处理用户命令、并返回结果 )
│   ├── common.py             公共函数模块  ( 登录密码加密、输入验证等公共模块 )
│   ├── myexception.py        自定义异常模块 （业务处理异常的自定义异常类）
│   └── users.py              用户类模块
└── sshkey                   私钥方式登录的私钥保存目录

五、命令介绍
  1 help
    查看系统命令信息

  2 show [hosts -a | -g gid ],[groups]
    查看用户的管理的组及组对应服务器信息
      e.g: show groups        查看组信息
           show hosts -a      查看所有服务器信息
           show hosts -g G01  查看服务器组 G01 下的所有服务器信息

  3 cmd [-h ipaddress | -g gid] -c command
    批量执行命令
      e.g: cmd -h 192.168.1.128 -c "df -hl"   访问远程服务器192.168.1.128执行df -hl 返回结果
           cmd -g G01 -c "df -hl"             批量访问组 G01 下的所有服务器 执行 df -hl 返回结果

  4 sftp [-u | -d] [-h ipaddr | -g gid] -s filepath -t filepath
    上传或下载文件
          -u 上传文件
          -d 下载文件
          -s 源文件地址
          -t 目的地址文件
     e.g: sftp -u -g G01 -s /tmp/aaa -t /tmp/aaa

六 程序运行结果展示:

1: 登录

super@ubuntu:~/PycharmProjects/Day8$ python3 main.py

-----------------------------------------
|             简版堡垒机                |
-----------------------------------------

用户名: test
密码:
欢迎登录堡垒机精简版(v1.0)

[ test ] (q to exit):\>

2： help命令

[ test ] (q to exit):\> help
-------------------------------  help list  ----------------------------------------------
    command:
        help:
        show:  show [hosts -a | -g gid ],[groups]         # 查看用户的管理的组及组对应服务器信息 e.g: show groups, show hosts -a
        cmd:   cmd [-h ipaddress | -g gid] -c command     # 批量执行命令 e.g: cmd -g G01 -c "df -hl"
        sftp:  sftp [-u | -d]                             # 上传或下载文件 -u update -d download
                    [-h ipaddr | -g gid]                  # -s 原文件地址  -t 目的地址文件
                    -s filepath -t filepath               # e.g: sftp -u -g G01 -s /tmp/aaa -t /tmp/aaa

3： show命令

[ test ] (q to exit):\> show groups
 GID: G01, GNAME: 新闻组;
 GID: G02, GNAME: 视频组;

[ test ] (q to exit):\> show hosts -a

IP: 192.168.2.128  主机名: agent  所属组ID: G01 ;
IP: 192.168.2.129  主机名: ubuntu  所属组ID: G01 ;
IP: 192.168.1.128  主机名: agent  所属组ID: G02 ;

[ test ] (q to exit):\> show hosts -g G01

IP: 192.168.2.128  主机名: agent  所属组ID: G01 ;
IP: 192.168.2.129  主机名: ubuntu  所属组ID: G01 ;

4：cmd命令

[ test ] (q to exit):\> cmd -g G01 -c "ls -l /tmp"
 IP -> 192.168.2.129 :
total 28
-rw------- 1 super super    0 Mar 10 17:43 config-err-xiu4ci
drwx------ 2 super super 4096 Mar 10 17:43 ssh-lxnpFuoOxn7M
drwx------ 3 root  root  4096 Mar 10 17:42 systemd-private-4612a8a4a54946a79a8e9a1ca72eac43-colord.service-bWT701
drwx------ 3 root  root  4096 Mar 10 17:42 systemd-private-4612a8a4a54946a79a8e9a1ca72eac43-rtkit-daemon.service-GcRE5e
drwx------ 3 root  root  4096 Mar 10 17:42 systemd-private-4612a8a4a54946a79a8e9a1ca72eac43-systemd-timesyncd.service-cCXzLk
drwx------ 2 super super 4096 Mar 10 17:43 tracker-extract-files.1000
drwxrwxrwt 2 root  root  4096 Mar 10 17:42 VMwareDnD
drwx------ 2 root  root  4096 Mar 10 17:42 vmware-root

# 128服务器未启动
Unable to connect to 192.168.2.128: [Errno 113] No route to host
2016-03-10 18:03:54,313 - ERROR - Unable to connect to 192.168.2.128: [Errno 113] No route to host

5：sftp命令

 test ] (q to exit):\> sftp -u -g G01 -s /home/super/testfolder/up -t /tmp/sftp-up.test

 local[ /home/super/testfolder/up ] >>>>> upload to >>>>>> 192.168.2.129[ /tmp/sftp-up.test ]   finished

 local[ /home/super/testfolder/up ] >>>>> upload to >>>>>> 192.168.2.128[ /tmp/sftp-up.test ]   finished