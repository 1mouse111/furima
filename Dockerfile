# ベースとなるPython環境
FROM python:3.13-slim

# 作業ディレクトリを指定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit用のポートを開ける
EXPOSE 8501

# コンテナ起動時に実行されるコマンド
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]

