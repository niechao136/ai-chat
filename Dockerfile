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

# install nginx and tini
RUN apt-get update && apt-get install -y nginx tini && rm -rf /var/lib/apt/lists/*

# copy backend
COPY . .
# Set default environment variables
ENV SECRET_KEY=my-very-secret-dev-key-12345678
ENV GEMINI_API_KEY=AIzaSyC9zfYBsVwF9RUGgK_hgCukCxS8DmfLYOw

# Copy frontend build: explicitly copy the build artifacts to Nginx directory
# Fix: The build directory is /app/out, not /app/frontend/out
COPY --from=frontend-build /app/out /usr/share/nginx/html

# copy nginx config
COPY nginx.conf /etc/nginx/sites-available/default
# Link to enabled sites
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

EXPOSE 8000 80
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/start.sh"]
