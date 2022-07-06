"""
dict客户端
功能：根据用户输入，发送请求，得到结果
结构：一级界面 --> 注册  登录  退出
    二级界面 --> 查询  历史  注销
"""
import sys
from socket import *
from getpass import getpass


# 服务器地址
ADDR = ('127.0.0.1',8000)
# tcp套接字
s = socket()
s.connect(ADDR)


# 查单词
def do_query(name):
    while True:
        word = input("请输入单词：")
        if not word:
            return
        s.send(("Q %s %s"%(name,word)).encode())
        # 等待反馈
        data = s.recv(2048).decode()
        print(data)
        print("\r\n\r\n")


# 历史记录
def do_history(name):
    msg = "H "+name
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data =="OK":
        while True:
            data = s.recv(2048).decode()
            if data =="##":
                break
            print(data)
    else:
        print("您没有历史记录")



# 二级界面--登录后的状态
def login(name):
    while True:
        print("""
        ==================Query=================
            1.查词        2.历史        3.注销
        """)

        cmd = input("请选择功能：")
        if cmd=='1':
            do_query(name)
        elif cmd =="2":
            do_history(name)
        elif cmd=='3':
            return
        else:
            print("请输入正确选项")


# 注册函数
def do_register():
    while True:
        user = input("请输入用户名：")
        password = getpass("请输入密码：")
        password2 = getpass("再次输入密码：")
        if password != password2:
            print("两次密码不一致，重新注册\r\n")
            continue
        if ' ' in user or ' 'in password:
            print("用户名或密码不能包含空格\r\n")
            continue

        msg = "R %s %s"%(user,password)
        s.send(msg.encode())  # 发送给服务器
        data = s.recv(1024).decode()
        if data =="OK":
            print("注册成功")
            login(user)
        else:
            print("注册失败",data)
        return

# 登录
def do_login():
    user = input("请输入用户名：")
    password = getpass("请输入密码：")
    msg = "L %s %s"%(user,password)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data =="OK":
        print("登录成功")
        login(user)
    else:
        print(data)


# 搭建客户端网络
def main():
    while True:
        print("""
        ================welecome================
            1.注册        2.登录        3.退出
        """)

        cmd = input("请选择功能：")
        if cmd=='1':
            do_register()
        elif cmd =="2":
            do_login()
        elif cmd=='3':
            s.send(b'E')
            sys.exit("感谢使用")
        else:
            s.send(cmd.encode())

if __name__ == '__main__':
    main()