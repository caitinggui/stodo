# stodo
A web based on sanic and made for todo list management.


## 数据库选择

考虑到本人的服务器性能不足，所以用sqlite3，采用aioodbc作为连接，
aioodbc基于pyodbc，遵循ODBC协议，在linux上需要安装odbc驱动,步骤如下：
- 安装ODBC驱动
    - centos中: `$ sudo yum install unixODBC unixODBC-devel libtool-ltdl libtool-ltdl-devel`
    - ubuntu中: `sudo apt install unixodbc-dev libsqlite3-dev sqlite3`
- 安装sqlite3的odbc驱动
    - `$ git clone https://github.com/softace/sqliteodbc.git`
    - `$ cd sqliteodbc`
    - `$ ./configure && make`
    - `$ sudo make install`    # 到这里就成功安装了驱动，接下来要配置驱动
    - `$ odbcinst -j`          # 查看系统的odbc配置
    - `$ sudo vim /etc/odbcinst.ini`  # 添加如下内容, Driver的路径自己检查一下有没有
        -    [SQLite]  
		     Description=SQLite ODBC Driver  
		     Driver=/usr/local/lib/libsqlite3odbc.so 
		     Setup=/usr/local/lib/libsqlite3odbc.so
		     Threading=20

到此，驱动安装成功，这里也可以将sqlite3换成MySQL，然后采用aiomysql(ps:aioodbc也支持mysql)


## 环境变量
可以在virtual生成的环境中设置一些常用的环境变量(在env/bin/activate中export)

`export PYTHONDONTWRITEBYTECODE=1`关闭python3编译生成的`__pycache__`

设置`export alias "stodo"="python /your/path/to/stodo_server.py"`
