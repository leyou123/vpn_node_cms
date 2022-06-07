#### 启动脚本

节点后台启动 服务

```
# 拉取git代码
git clone https://github.com/yanjigame/vpn_node_cms.git

# 启动单个服务
nohup python3 /root/vpn_node_cms/manage.py runserver 0.0.0.0:9000> /root/vpn_node_log.txt 2>&1 &
```

```
# 生成静态文件
python3 /root/vpn_node_cms/manage.py collectstatic

# 启动
/usr/local/python3/bin/uwsgi --ini /root/vpn_node_cms/uwsgi.ini  
# 停止
/usr/local/python3/bin/uwsgi --stop /root/vpn_node_cms/uwsgi.pid
# 重启
/usr/local/python3/bin/uwsgi --reload /root/vpn_node_cms/uwsgi.pid
```


后台脚本启动
```
# 检测用户流量
nohup python3 /root/vpn_node_cms/Script/check_user_flow.py > /root/check_user_flow.txt 2>&1 &
```


