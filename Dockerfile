# build frontend
FROM node:22-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN pnpm run build

# build backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nginx tini && rm -rf /var/lib/apt/lists/*

# Assuming the static files are generated in /app/out by the Next.js static export
COPY --from=frontend-build /app/frontend/out /usr/share/nginx/html

COPY . .
COPY nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

EXPOSE 8000 80
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/start.sh"]
