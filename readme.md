## 电子词典

- **数据库mysql格式：**
  - dict
      - words 
          - `CREATE TABLE 'words' (
    'id' int NOT NULL AUTO_INCREMENT,
    'word' char(32) DEFAULT NULL,
    'mean' text,
    PRIMARY KEY ('id')
  )`
      - user
          - `CREATE TABLE 'user' (
    'id' int NOT NULL AUTO_INCREMENT,
    'name' varchar(32) NOT NULL,
    'password' varchar(128) NOT NULL,
    PRIMARY KEY ('id')
  )`
      - history
          - `CREATE TABLE 'history' (
    'id' int NOT NULL AUTO_INCREMENT,
    'name' varchar(32) NOT NULL,
    'word' varchar(28) NOT NULL,
    'time' datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ('id')`
  )
          
- **数据库导入**
  - mysql -u [user] -p dict < words.sql
  
- **启动**
  1. 运行 server.py
  2. 运行 client.py