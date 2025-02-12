# PDF to Page Images Agent Example

PDFファイルをページごとの画像に変換するLangChainエージェントのサンプル実装です。

## セットアップ

1. 環境変数の設定:
```bash
cp .env.sample .env
# .envファイルを編集して必要なAPIキーを設定
```

2. 依存関係のインストール:
```bash
pip install -e .
```

## 使用例

```python
from middleman_ai import ToolsClient
from pdf_to_images_agent.agent import create_agent

# Middleman.aiクライアントの初期化
client = ToolsClient(api_key="YOUR_API_KEY")

# エージェントの作成
agent = create_agent(client=client)

# PDFを画像に変換
response = agent.invoke({
    "input": "sample.pdfファイルを画像に変換してください"
})
print(f"Agent response: {response}")
```
