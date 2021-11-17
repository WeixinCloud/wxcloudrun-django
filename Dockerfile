# 写在最前面：强烈建议先阅读官方教程[Dockerfile最佳实践]（https://docs.docker.com/develop/develop-images/dockerfile_best-practices/）
# 选择构建用基础镜像（选择原则：在包含所有用到的依赖前提下尽可能提及小）。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/golang?tab=tags)自行选择后替换。
FROM python:3.7.3 AS build

# 创建临时依赖下载文件夹
RUN mkdir /install

# 设置当前下载依赖的文件夹
WORKDIR /install

# 拷贝依赖文件
COPY requirements.txt /requirements.txt

# 安装依赖到指定的/install文件夹
RUN pip install --upgrade pip \
&& pip install --prefix=/install -r /requirements.txt

# 选择基础镜像
FROM python:3.7.3-alpine

# 拷贝下载好的依赖到alpine镜像的/use/local文件夹下
COPY --from=build /install /usr/local

# 拷贝当前项目到/app目录下
COPY . /app

# 设定当前的工作目录
WORKDIR /app

# 设定对外端口
EXPOSE 80

# 设定启动命令
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:80"]
