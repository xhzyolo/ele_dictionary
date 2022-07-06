"""
数据库模块
将数据库操作封装一个类，将server需要的数据库操作功能分别写成方法，
在server中实例化对象，需要什么方法直接调用
"""

import pymysql
import hashlib


# 加密算法
SALT = "#Ypwd&"

class Database:
    def __init__(self,host='localhost',
                 port = 3306,
                 user = 'root',
                 password = '123456',
                 charset = 'utf8',
                 database=None):
        self.host=host
        self.port = port
        self.user=user
        self.password = password
        self.charset=charset
        self.database = database
        self.connect_database()

    # 连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset
                                  )

    # 关闭数据库
    def close(self):
        self.db.close()

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 密码加密
    def hash_pwd(self, name, password):
        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())
        return hash.hexdigest()

    # 注册操作
    def register(self,name,password):
        sql = "select * from user where name='%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:  # 如果找到说明用户存在，不允许注册，返回Fasle
            return False

        password = self.hash_pwd(name, password)

        # 插入数据库
        sql = "insert into user (name,password) values (%s,%s)"

        try:
            self.cur.execute(sql,[name,password])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)
            return False
    # 登录处理
    def login(self,name,password):
        password = self.hash_pwd(name,password)
        sql = "select * from user where name = '%s' and password = '%s'"%(name,password)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 查单词
    def query(self,word):
        sql = "select mean from words where word='%s'"%word
        self.cur.execute(sql)
        mean = self.cur.fetchone()
        if mean:
            return mean[0]
        # else:  可以不写 默认返回 None
        #     return None

    # 插入历史记录
    def insert_history(self,name,word):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    # 查询历史
    def history(self,name):
        sql = "select name,word,time from history where name = '%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()
