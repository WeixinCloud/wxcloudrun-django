# 写在最前面：强烈建议先阅读官方教程[Dockerfile最佳实践]（https://docs.docker.com/develop/develop-images/dockerfile_best-practices/）
# 选择构建用基础镜像（选择原则：在包含所有用到的依赖前提下尽可能提及小）。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。
FROM python:3.8.12 as builder

# 指定构建过程中的工作目录
WORKDIR /app

# 安装最新python依赖管理工具pip
RUN pip install --upgrade pip

# 复制python依赖模块列表到工作目录
COPY requirements.txt /app/

# 使用依赖管理工具安装依赖
RUN pip install -r requirements.txt


# 选用运行时所用基础镜像（选择原则：尽量体积小、包含基础linux内容的基础镜像）
FROM python:3.8-slim-buster

# 指定构建过程中的工作目录
WORKDIR /app

# 拷贝编译好的库复制到运行时所用基础镜像
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

#将当前目录（dockerfile所在目录）下所有文件都拷贝到工作目录下
COPY . /app/

# 执行启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
