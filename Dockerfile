FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p data/logs data/templates

# 设置环境变量
ENV PORT=5000

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "run.py"]