FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 👇 .env をコンテナ内に含める

COPY . .

RUN mkdir -p /tmp/interview_ai_shared

EXPOSE 5000

# 環境変数（任意、FLASK_* はgunicornでは実質使われない）
ENV FLASK_ENV=production

# ✅ gunicorn で Flask アプリを起動（app.py 内の admin_app を使用）
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "-w", "4", "-k", "gevent"]
