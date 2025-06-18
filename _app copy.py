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

# Azure OpenAI クライアント初期化
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)


@app.route("/")
def main_page():
    return render_template("dashboard.html")

    # return render_template("request_approval.html")

@app.route("/view_page")
def view_page():
    return render_template("view_page.html")

@app.route("/generate", methods=["POST"])
def generate():

    # テキストファイルを読み込む
    with open("input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    user_input = input_text
    user_input = "下の文章をそのまま出力してください。\n\n 「以下がそのまま出力した文章です」などのコメントは出さずに、そのまま出力してください。" + user_input

    def stream():
        response = client.chat.completions.create(
            model="gpt-4o",  # ← Azureポータルで設定した「デプロイ名」に置き換えてください
            messages=[{"role": "user", "content": user_input}],
            temperature=0.7,
            stream=True,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
            print(chunk)
    return Response(stream_with_context(stream()), content_type="text/event-stream")

## 実行
if __name__ == "__main__":
    app.run(debug=True)