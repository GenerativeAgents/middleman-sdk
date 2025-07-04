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
pdf_url = client.md_to_pdf(markdown_text, pdf_template_id="template-uuid")
print(f"Generated PDF URL: {pdf_url}")
```

## CLI の使用方法

SDK はコマンドラインインターフェース（CLI）も提供しています。UV を使用して以下のように実行できます：

```bash
# APIキーの設定
export MIDDLEMAN_API_KEY=your-api-key

# Markdown → PDF変換
echo "# テスト" | uvx middleman md-to-pdf [テンプレートID]

# Markdown → DOCX変換
echo "# テスト" | uvx middleman md-to-docx

# PDF → ページ画像変換
uvx middleman pdf-to-page-images input.pdf

# DOCX → ページ画像変換
uvx middleman docx-to-page-images input.docx

# PPTX → ページ画像変換
uvx middleman pptx-to-page-images input.pptx

# XLSX → ページ画像変換
uvx middleman xlsx-to-page-images input.xlsx

# PPTXテンプレート解析
uvx middleman json-to-pptx-analyze [テンプレートID]

# PPTXテンプレート実行
echo '{"slides":[{"type":"title","placeholders":[{"name":"title","content":"テストタイトル"}]}]}' | \
uvx middleman json-to-pptx-execute [テンプレートID]

# Mermaid図表 → 画像変換
echo "graph TD; A-->B" | uvx middleman mermaid-to-image
```

各コマンドは標準入力からテキストを受け取るか、必要に応じてファイルパスやテンプレート ID を引数として受け取ります。

## MCP Server

Middleman SDK は MCP サーバーを提供し、Claude Desktop アプリケーションなどから利用できます。

### Claude Desktop 設定

Claude Desktop アプリケーションの`claude_desktop_config.json`を以下のように設定します：

```json
{
  "mcpServers": {
    "middleman": {
      "command": "uvx",
      "args": ["--from", "middleman-ai", "mcp-server"],
      "env": {
        "MIDDLEMAN_API_KEY": "xxxxx"
      }
    }
  }
}
```

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
