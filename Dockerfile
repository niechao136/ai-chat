# build frontend
FROM node:18-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ ./
# 使用 build 进行构建
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

# Copy frontend build: explicitly copy the build artifacts to Nginx directory
# Next.js default output is in frontend/.next
# To serve via Nginx, we need the exported static files
RUN mkdir -p /usr/share/nginx/html && \
    cp -r frontend/.next/static /usr/share/nginx/html/_next/static && \
    cp -r frontend/public/* /usr/share/nginx/html/ || true

# copy nginx config
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 8000 80
CMD ["sh", "-c", "service nginx start && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
