# stodo
A web based on sanic and made for todo list management.

## 环境变量
可以在virtual生成的环境中设置一些常用的环境变量(在env/bin/activate中export)
- `export PYTHONDONTWRITEBYTECODE=1`    # 关闭python3编译生成的`__pycache__`
- `export alias "stodo"="python /your/path/to/stodo_server.py"`  # 可以使用`$ stodo initdb`来初始化数据库
- `export SECRET_KEY='your secret key'`  # 不要在配置中直接写，容易暴露
