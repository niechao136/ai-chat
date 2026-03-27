#!/bin/sh
set -e

# 符号链接 Nginx 日志到标准输出
ln -sf /dev/stdout /var/log/nginx/access.log
ln -sf /dev/stderr /var/log/nginx/error.log

# 启动 Nginx
nginx -g "daemon on;"

# 定义优雅退出函数
cleanup() {
    echo "Shutting down..."
    nginx -s quit
    kill -TERM "$uvicorn_pid" 2>/dev/null
    exit 0
}

# 捕获终止信号
trap cleanup SIGTERM SIGINT

# 启动 FastAPI，并记录其 PID
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
uvicorn_pid=$!

# 等待 Uvicorn 退出，或者 Nginx 崩溃
while kill -0 "$uvicorn_pid" 2>/dev/null; do
    if ! pgrep -x "nginx" >/dev/null; then
        echo "Nginx died, exiting..."
        exit 1
    fi
    sleep 2
done

cleanup
