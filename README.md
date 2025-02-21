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
echo "# テスト" | uvx middleman md_to_pdf

# Markdown → DOCX変換
echo "# テスト" | uvx middleman md_to_docx

# Markdown → PPTX変換
echo "# テスト" | uvx middleman md_to_pptx

# PDF → ページ画像変換
uvx middleman pdf_to_page_images input.pdf

# PPTXテンプレート解析
uvx middleman json_to_pptx_analyze [テンプレートID]

# PPTXテンプレート実行
echo '{"slides":[{"type":"title","placeholders":[{"name":"title","content":"テストタイトル"}]}]}' | \
uvx middleman json_to_pptx_execute [テンプレートID]
```

各コマンドは標準入力からテキストを受け取るか、必要に応じてファイルパスやテンプレートIDを引数として受け取ります。

## LangChain との統合

```python
from langchain_core.agents import AgentExecutor
from langchain_core.language_models import BaseLanguageModel
from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.md_to_pdf import MdToPdfTool

# Middleman.aiクライアントの初期化
client = ToolsClient(api_key="YOUR_API_KEY")

# LangChainツールの設定
md_to_pdf_tool = MdToPdfTool(client=client)

# LLMの設定
llm: BaseLanguageModel = ...  # お好みのLLMを設定

# エージェントの初期化
agent = AgentExecutor.from_agent_and_tools(
    agent=...,  # お好みのエージェントを設定
    tools=[md_to_pdf_tool],
    verbose=True
)

# 自然言語でPDF生成を実行
response = agent.invoke({"input": "以下のMarkdownテキストをPDFにして：# Title\nHello!"})
print(f"Agent response: {response}")
```

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
