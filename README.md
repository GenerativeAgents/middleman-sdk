# Middleman.ai Python SDK

Middleman.ai の API を簡単に利用するための Python SDK です。マークダウン →PDF 変換、JSON→PPTX 変換、PDF ページ → 画像変換などの機能を提供します。

## インストール

```bash
pip install middleman-ai
```

## 基本的な使い方

```python
from middleman_ai import ToolsClient

# クライアントの初期化
client = ToolsClient(api_key="YOUR_API_KEY")

# Markdown → PDF変換
markdown_text = "# Sample\nThis is a test."
pdf_url = client.md_to_pdf(markdown_text)
print(f"Generated PDF URL: {pdf_url}")
```

## CLIの使用方法

SDKはコマンドラインインターフェース（CLI）も提供しています。UVを使用して以下のように実行できます：

```bash
# APIキーの設定
export MIDDLEMAN_API_KEY=your-api-key

# Markdown → PDF変換
echo "# テスト" | uvx middleman md-to-pdf

# Markdown → DOCX変換
echo "# テスト" | uvx middleman md-to-docx

# Markdown → PPTX変換
echo "# テスト" | uvx middleman md-to-pptx

# PDF → ページ画像変換
uvx middleman pdf-to-page-images input.pdf

# PPTXテンプレート解析
uvx middleman json-to-pptx-analyze [テンプレートID]

# PPTXテンプレート実行
echo '{"slides":[{"type":"title","placeholders":[{"name":"title","content":"テストタイトル"}]}]}' | \
uvx middleman json-to-pptx-execute [テンプレートID]
```

各コマンドは標準入力からテキストを受け取るか、必要に応じてファイルパスやテンプレートIDを引数として受け取ります。

## 機能一覧

- Markdown → PDF 変換
- Markdown → DOCX 変換
- Markdown → PPTX 変換
- PDF → ページ画像変換
- JSON → PPTX 変換（テンプレート解析・実行）

## エラーハンドリング

```python
from middleman_ai import ToolsClient, NotEnoughCreditError

client = ToolsClient(api_key="YOUR_API_KEY")

try:
    pdf_url = client.md_to_pdf("# Test")
except NotEnoughCreditError:
    print("クレジット不足です。プランをアップグレードしてください。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
```

## ライセンス

MIT License
