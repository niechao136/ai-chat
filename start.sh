#!/bin/sh
set -e

# Link Nginx logs to stdout/stderr
ln -sf /dev/stdout /var/log/nginx/access.log
ln -sf /dev/stderr /var/log/nginx/error.log

# Start FastAPI (listen on 8000)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
uvicorn_pid=$!

# Start Nginx in foreground (daemon off)
# This makes Nginx the primary process
nginx -g "daemon off;" &
nginx_pid=$!

# Cleanup function
cleanup() {
    echo "Shutting down..."
    kill -TERM "$uvicorn_pid" 2>/dev/null
    kill -TERM "$nginx_pid" 2>/dev/null
    wait "$uvicorn_pid" "$nginx_pid" 2>/dev/null
    exit 0
}

# Trap signals
trap 'cleanup' TERM INT

# Monitor processes
while kill -0 "$uvicorn_pid" 2>/dev/null && kill -0 "$nginx_pid" 2>/dev/null; do
    sleep 2
done

echo "A process died. Exiting..."
cleanup
