from flask import Flask,render_template,request, redirect, url_for, session, Response, stream_with_context

import csv
import pandas as pd
import numpy as np
import time
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import io


app = Flask(__name__)

# 環境変数を読み込む
load_dotenv()

global_model = "o3"
#global_model = "gpt-4o"

if global_model == "o3":
    client = AzureOpenAI(
        api_key=os.getenv("O3_AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("O3_AZURE_OPENAI_ENDPOINT"),
        api_version="2024-12-01-preview",
    )


else:
    print("Using GPT-4o model")
    print(os.getenv("4O_AZURE_OPENAI_ENDPOINT"))
    # Azure OpenAI クライアント初期化
    client = AzureOpenAI(
        api_key=os.getenv("4O_AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("4O_AZURE_OPENAI_ENDPOINT"),
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
    data = request.get_json(silent=True) or {}
    department = data.get("department", "全て")

    df = pd.read_csv("static/data/data/taishoku_data.csv")

    # 部署でフィルタ（「全て」はそのまま）
    if department != "全て":
        df = df[df["所属部署"] == department]

    # フィルタ後を文字列化してプロンプトに渡す
    csv_text = df.to_csv(index=False)
    print("CSV Text:", csv_text)


    user_input = f"""あなたはデータサイエンティスト兼人的資本経営の専門家です。
                    アップロードする **退職者に関する従業員データ (UTF-8, カンマ区切り, ヘッダー行あり)** を分析し、以下の観点で洞察を提示してください。

                    -- 分析観点 --
                    1. 退職者の基本傾向
                        - 退職者数、年齢分布、性別比率、部署比率、ランク比率、勤続年数、退職理由の項目ごとに簡潔に結果を記載
                        - それぞれの項目について、各1行で基本傾向を記載してください。
                        - 例: 「30代の男性が最も多く、全体の40%を占める」など
                    2. 離職要因の深堀分析
                        - 年齢、性別、勤続年数、部署、ランクなどの特徴量を用いて、各セグメントごとの退職理由を調査
                        - 例: 「30代男性の離職理由はキャリアアップが80%」など
                    3. 解決すべき課題と解決策の提案（実行可能なアクション含む）
                        - 退職者の傾向や離職要因を踏まえ、組織が直面している課題を特定し、それに対する解決策を提案
                        - 課題の特定をする際は、「2.離職要因の深堀分析」の結果を引用してください。
                        - 例: 「30代男性のキャリアアップ志向に応えるための研修プログラムの導入」など

                    -- 注意点 --
                    出力は **Markdown** で、読みやすさを意識して絵文字・太字などを適宜活用してください。
                    Pythonコードは分析に使用して構いませんが、Python コードは出力に含めないでください。

                    -- CSVデータの内容は以下の通りです。CSVのヘッダーは「社員ID,氏名,退職日,入社日,勤続年数,所属部署,ランク,性別,年齢,前職,入社区分,退職理由カテゴリ,退職理由自由記述」です。--
                    {csv_text}
                    """ 
       
    def stream():
        response = client.chat.completions.create(
            model=global_model,  # ← Azureポータルで設定した「デプロイ名」に置き換えてください
            messages=[{"role": "user", "content": user_input}],
            stream=True,
            temperature=1.0,  # 温度パラメータを設定
            top_p=1.0,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    return Response(stream_with_context(stream()), content_type="text/event-stream")

## 実行
if __name__ == "__main__":
    print("---------------------")
    print("使用しているモデルは、", global_model)
    print("---------------------")
    app.run(debug=True)