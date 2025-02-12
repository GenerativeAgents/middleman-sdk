# JSON to PPTX Agent

ユーザーから依頼された内容を JSON 形式に整形し、PPTX に変換するエージェントのサンプルです。

## 必要条件

- Python 3.10 以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:

```bash
git clone [repository-url]
cd examples/json_to_pptx_agent
```

2. 環境変数の設定:

```bash
cp .env.sample .env
```

`.env`ファイルを編集し、必要な API key を設定してください：

- `MIDDLEMAN_API_KEY`: Middleman.ai の API キー
- `MIDDLEMAN_TEMPLATE_ID`: Middleman.ai のテンプレート ID （[こちら](./sample_template.pptx)にテンプレートサンプルがあります）
- `OPENAI_API_KEY`: OpenAI の API キー

3. 依存関係のインストール:

```bash
uv sync
```

## 使用方法

1. サンプルスクリプトの実行:

```bash
uv run python -m src.json_to_pptx_agent.agent
```

生成された PPTX の URL がエージェントからの出力として表示されます。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。
