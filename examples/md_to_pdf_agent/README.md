# Markdown to PDF Agent

ユーザーから依頼された内容を Markdown 形式に整形し、PDF に変換するエージェントのサンプルです。

## 必要条件

- Python 3.10 以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:

```bash
git clone [repository-url]
cd examples/md_to_pdf_agent
```

2. 環境変数の設定:

```bash
cp .env.sample .env
```

`.env`ファイルを編集し、必要な API key を設定してください：

- `MIDDLEMAN_API_KEY`: Middleman.ai の API キー
- `OPENAI_API_KEY`: OpenAI の API キー

3. 依存関係のインストール:

```bash
uv sync
```

## 使用方法

1. サンプルスクリプトの実行:

```bash
uv run python -m src.md_to_pdf_agent.agent
```

生成された PDF の URL がエージェントからの出力として表示されます。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。
