# ai-dashboard

## 概要

**ai-dashboard** は、退職者に関する従業員データ（CSV）をアップロードし、Azure OpenAI（GPT-4o等）を活用して多角的に分析・可視化するダッシュボード型Webアプリケーションです。  
Python（Flask）で構築されており、Azure OpenAIのAPIを利用して、退職傾向や要因分析、改善提案などをMarkdown形式で出力します。

---

## ディレクトリ構成

```
.
├── app.py                      # Flaskアプリ本体
├── requirements.txt            # 依存パッケージ
├── Dockerfile                  # Dockerビルド用
├── docker-compose.yml          # Docker Compose定義
├── .env                        # 環境変数（APIキー等、git管理外）
├── static/
│   ├── css/                    # CSSファイル
│   ├── images/                 # 画像ファイル
│   └── data/
│       └── data/
│           ├── taishoku_data.csv         # 分析用CSVデータ
│           └── taishoku_data_bkup.csv    # バックアップ
├── templates/
│   ├── layout.html
│   └── dashboard.html
└── README.md
```

---

## 必要な環境変数

`.env` ファイルをプロジェクトルートに作成し、以下の内容を記載してください。

```env
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
```

---

## ローカルでの実行方法

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. Flaskアプリの起動

```bash
python app.py
```

- ブラウザで [http://localhost:5000](http://localhost:5000) にアクセス

---

## Dockerによる実行

### 1. Dockerイメージのビルド

```bash
docker build -t ai-dashboard .
```

### 2. Dockerコンテナの起動

```bash
docker run --env-file .env -p 5000:5000 ai-dashboard
```

---

## docker-composeによる実行

```bash
docker-compose up --build
```

---

## Azure Container Registry (ACR) へのpush手順

> **注意:**  
> Docker Desktop などの Docker クライアントがインストールされ、起動している必要があります。  
> インストールされていない場合は [公式サイト](https://www.docker.com/products/docker-desktop/) からインストールしてください。

1. **ACRへログイン**

```bash
az acr login --name <your-acr-name>
```

2. **イメージにタグ付与**

```bash
docker tag ai-dashboard <your-acr-name>.azurecr.io/ai-dashboard:latest
```

3. **イメージをACRへpush**

```bash
docker push <your-acr-name>.azurecr.io/ai-dashboard:latest
```

---

## Azure上でのデプロイ手順（例: Azure Web App for Containers）

1. **AzureポータルでWeb App for Containersを作成**
   - コンテナイメージとして `<your-acr-name>.azurecr.io/ai-dashboard:latest` を指定
   - 環境変数（AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT）を設定

2. **起動後、WebアプリのURLにアクセスし動作確認**

---

## 注意事項

- .envファイルやAPIキーはgit管理しないでください。
- Azure OpenAIのAPIキー・エンドポイントは有効なものを用意してください。
- データファイル（CSV）は `static/data/data/taishoku_data.csv` を参照しています。
- **ACRへのpushやpullにはDockerが必須です。エラー例: `DOCKER_COMMAND_ERROR` が出る場合は、Dockerがインストール・起動されているか確認してください。**

---

## 開発者情報

- 開発者: 吉田高志
- 所属: AI Leap Sector
- Email: takashiyoshida@abeam.com

---
