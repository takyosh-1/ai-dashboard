from flask import Flask,render_template,request, redirect, url_for, session, Response, stream_with_context, jsonify

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
    api_version="2024-12-01-preview",
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
    request_data = request.get_json() or {}
    selected_department = request_data.get('department', 'all')
    selected_model = request_data.get('model', 'o3')

    print(f"Selected department: {selected_department}, Selected model: {selected_model}")

    # テキストファイルを読み込む
    with open(r"static\data\data\taishoku_data.csv", "r", encoding="utf-8") as file:
        input_text = file.read()

    department_filter_text = ""
    if selected_department != "all":
        department_names = {
            "sales": "営業",
            "marketing": "マーケ"
        }
        dept_name = department_names.get(selected_department, selected_department)
        department_filter_text = f"\n\n特に「{dept_name}」部署のデータに焦点を当てて分析してください。"
    
    user_input = """あなたはデータサイエンティストであり、人的資本経営に詳しい専門家です。
                    以下に、退職者に関する従業員データ（CSV）をアップロードします。
                    このデータを分析し、下に示した観点で分析してください。
                    出力形式はMarkdown形式で、構造化してわかりやすく記述してください。
                    なお、Pythonコードの使用も可能です。

                    -- 分析観点 --
                    ・退職者の基本的な傾向分析（年齢、性別、勤続年数など）
                    ・離職率に関係しそうな重要な特徴の特定（要因分析）
                    ・そこから導かれる示唆・仮説
                    ・離職を減らすために注力すべき課題の特定
                    ・解決策の提案（実行可能なアクション含む）

                    -- CSVデータの内容は以下の通りです。CSVのヘッダーは「社員ID,氏名,退職日,入社日,勤続年数,所属部署,ランク,性別,年齢,前職,入社区分,退職理由カテゴリ,退職理由自由記述」です。--
                    """ + department_filter_text + "\n\n" + input_text

    print(user_input)

    def stream():
        try:
            response = client.chat.completions.create(
                model=selected_model,  # 選択されたモデルを使用
                messages=[{"role": "user", "content": user_input}],
                stream=True,
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error with model {selected_model}: {str(e)}")
            yield f"エラーが発生しました。モデル '{selected_model}' が利用できない可能性があります。"
    return Response(stream_with_context(stream()), content_type="text/event-stream")

## 実行
if __name__ == "__main__":
    print(os.getenv("AZURE_OPENAI_ENDPOINT"))
    app.run(debug=True)
