# stodo
A web based on sanic and made for todo list management.

## 部署说明

- 创建虚拟环境(指定为python3.4+)： `$ virtualenv --python=python3 env`
- 安装依赖包: `$ source env/bin/activate; pip install -r requirement.txt`
- 在MySQL中创建数据库`Stodo`, 配置在configs/test.py中
- 设置下面的环境变量
- 初始化数据库`(env) $ stodo initdb`
- 运行`(env) $ stodo run`

## 环境变量
可以在virtual生成的环境中设置一些常用的环境变量(在env/bin/activate中export)
- `export PYTHONDONTWRITEBYTECODE=1`    # 关闭python3编译生成的`__pycache__`
- `export alias "stodo"="python /your/path/to/stodo_server.py"`  # 可以使用`$ stodo initdb`来初始化数据库
- `export SECRET_KEY='your secret key'`  # 不要在配置中直接写，容易暴露
- `export MYSQL_PASSWORD='your password'`
