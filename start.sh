#!/bin/sh

# 使用VSCode的扩展Weixin Cloudbase Docker Extension进行本地调试. 该扩展2022/8/11发
# 布的2.2.56版本中, 直接Start容器时, 自动输入的docker run命令有误, -e参数后面应该直
# 接用无单引号形式, 例如 MYSQL_USERNAME=root, 而不是'MYSQL_USERNAME=root'. 因此,
# 如果需要连接远程MySQL数据库, 应使用Live Coding模式, 而在发布(推送到GitHub)前, 应
# 使用Start测试在未连接远程MySQL数据库的情况下, 代码能否正常运行, 因为线上版本并不是
# 用docker-compose(Live Coding模式)构建的, 而是使用docker run(Start模式)构建的.

# 收集静态文件到settings.py中的STATIC_ROOT目录, 添加--noinput参数来自动跳过是否覆盖
# 目录内文件的询问.
python3 manage.py collectstatic --noinput

# 在使用本地数据库./db.sqlite3和python3 manage.py runserver测试代码时, 已经运行过
# python3 manage.py makemigrations和migrate了, 现在使用远程MySQL数据库, 首先需要更
# 改settings.py中的DATABASE, 然后需要运行下面的命令, 将makemigrations生成的迁移文件
# 应用到MySQL数据库中.
python3 manage.py migrate


# Live Coding模式下, 检测到文件修改后会自动重启, 重新运行该shell文件, 此时该shell文件
# 应重启uwsgi, 一般无需重启nginx, 因为nginx一般在配置文件发生改变时重启, 但如需修改
# nginx的配置文件, 必须停止并重新构建镜像(Dockerfile中, 将配置文件COPY到默认目录).

# 启动uwsgi, 帮助web服务器(nginx)与django通信
if [ "$(ps -ef|grep  "uwsgi.ini"|grep -v grep)" ] # 如果uwsgi已启动
then
    uwsgi --stop ./logs/uwsgi.pid # 根据pid停止uwsgi
    while [ "$(ps -ef|grep  "uwsgi.ini"|grep -v grep)" ]
    do
        echo "waiting for uwsgi to stop"
        sleep 0.5
    done
fi
uwsgi uwsgi.ini #使用配置文件启动uwsgi

# 启动nginx, 直接提供静态资源服务, 其余的请求通过uwsgi最终发送至Django服务器
if [ "$(ps -ef|grep "nginx"|grep -v grep)" ] # 如果nginx已启动
then
    echo "nginx is already running" # 只是提示正在运行, 而不重启nginx
else
    # 注意: Start模式和线上发布时应将第一行注释, 改用第二行
    # nginx # 使用默认的后台运行模式启动nginx(Live Coding模式下使用)
    nginx -g "daemon off;" # 保持前台运行(不使用守护进程)
fi