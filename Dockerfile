# build frontend
FROM node:18-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ .
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
COPY --from=frontend-build /app/.next/static /usr/share/nginx/html/_next/static
COPY --from=frontend-build /app/public /usr/share/nginx/html/public
# Simplified: copy static files - Next.js needs a more complex export for full static
# Assuming static export or similar logic; for now, we'll serve everything from backend or Nginx
# To simplify, we keep the FastAPI mount for /static

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
