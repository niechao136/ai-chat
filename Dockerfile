# build frontend
FROM node:22-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ ./
# 使用 build 生成 dist
RUN pnpm run build

# build backend
FROM python:3.11-slim
WORKDIR /app

# install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# copy backend
COPY . .
# Explicitly set environment variables for pydantic
ENV SECRET_KEY=my-very-secret-dev-key-12345678
ENV OPENAI_API_KEY=sk-dummy



# Copy frontend build: explicitly copy the build artifacts to Nginx directory
RUN mkdir -p /usr/share/nginx/html && \
    cp -r frontend/out/* /usr/share/nginx/html/

# copy nginx config
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 8000 80
CMD ["sh", "-c", "service nginx start && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
