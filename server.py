"""
python 3.10
utf-8

dict服务端
功能：业务逻辑处理
模型：多进程tcp并发
"""
import sys
from socket import *
from multiprocessing import Process
import signal
from time import sleep

from mysql_control import Database

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
db = Database(database='dict',password='root')


# 服务端注册处理
def do_register(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    password = tmp[2]
    # 注册：返回True表示注册成功，False表示失败
    if db.register(name,password):
        c.send(b'OK')
    else:
        c.send(b'Fail')


# 登录
def do_login(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    password = tmp[2]
    if db.login(name,password):
        c.send(b'OK')
    else:
        c.send(b'Fail')

# 查询单词
def do_query(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]

    # 插入历史记录
    db.insert_history(name,word)

    # 没找到返回 None
    response = db.query(word)
    if response:
        msg = f"{word} : {response}"
        c.send(msg.encode())
    else:
        c.send('没有找到该单词'.encode())


# 历史记录
def do_history(c,data):
    name = data.split(" ")[1]
    hist = db.history(name)
    if hist:
        c.send(b'OK')
        for h in hist:
            # h --> (name,word,time)
            msg = "%s  %-16s %s"%h  # %-16s 左对齐 占16个宽度
            sleep(0.1)
            c.send(msg.encode())
        sleep(0.1)
        c.send(b'##')  # 结束标志
    else:
        c.send(b'Fail')


# 接收客户端请求，分配处理函数
def request(c):
    # 创建数据库游标 每个子进程单独生成
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)
        if not data or data[0] == 'E':
            sys.exit('客户端断开') # 对应的子进程退出
        if data[0] =='R':
            do_register(c,data)
        elif data[0] =='L':
            do_login(c,data)
        elif data[0] =='Q':
            do_query(c,data)
        elif data[0] =="H":
            do_history(c,data)



# 搭建网络
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print(f"Listen the port {PORT} ...")
    while True:
        try:
            c, addr = s.accept()
            print("Connect from ", addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        # 为客户端创建子进程
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
