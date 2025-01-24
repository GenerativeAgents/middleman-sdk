# Middleman.ai Python SDK

Middleman.aiのAPIを簡単に利用するためのPython SDKです。マークダウン→PDF変換、JSON→PPTX変換、PDFページ→画像変換などの機能を提供します。

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

## LangChainとの統合

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

- Markdown → PDF変換
- Markdown → DOCX変換
- Markdown → PPTX変換
- PDF → ページ画像変換
- JSON → PPTX変換（テンプレート解析・実行）

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

## 開発者向け情報

### テスト実行

```bash
pytest
```

### リンター実行

```bash
ruff check .
``` 