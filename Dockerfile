# build frontend
FROM node:18-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ ./
RUN pnpm run build

# build backend
FROM python:3.11-slim
WORKDIR /app

# install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install nginx to serve frontend
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# copy backend and frontend
COPY . .
# Copy frontend build to nginx html
RUN cp -r frontend/dist/* /usr/share/nginx/html/ || cp -r frontend/.next/* /usr/share/nginx/html/

EXPOSE 8000
CMD ["sh", "-c", "service nginx start && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
