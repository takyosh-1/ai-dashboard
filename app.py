from flask import Flask,render_template,request, redirect, url_for, session, Response, stream_with_context

import csv
import pandas as pd
import numpy as np
import time
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

# 環境変数を読み込む
load_dotenv()

# Azure OpenAI クライアント初期化 (テスト用にコメントアウト)
# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_version="2024-12-01-preview",
# )

@app.route("/")
def main_page():
    return render_template("dashboard.html")

    # return render_template("request_approval.html")

@app.route("/view_page")
def view_page():
    return render_template("view_page.html")

@app.route("/generate", methods=["POST"])
def generate():

    def stream():
        mock_response = """# 退職者データ分析結果


退職者データを分析した結果、以下の傾向が確認されました：

- **年齢層**: 20代後半から30代前半の退職が多い
- **勤続年数**: 2-3年での退職が最も多い
- **部署別**: 営業部門の離職率が高い


離職に関係する主要な要因：
1. キャリア成長の機会不足
2. ワークライフバランスの問題
3. 給与・待遇への不満


- メンター制度の導入
- フレックスタイム制度の拡充
- 定期的なキャリア面談の実施
"""
        
        for char in mock_response:
            time.sleep(0.02)  # 20ms間隔で文字を送信
            yield char
    return Response(stream_with_context(stream()), content_type="text/event-stream")

## 実行
if __name__ == "__main__":
    print(os.getenv("AZURE_OPENAI_ENDPOINT"))
    app.run(debug=True)
