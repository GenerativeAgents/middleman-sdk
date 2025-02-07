# Web Page to Slide

ウェブページの内容を自動的にパワーポイントスライドに変換するエージェントのサンプルです。

## 機能

- ウェブページのURLからコンテンツを抽出
- LLMを使用してコンテンツを解析し、スライド形式に最適化
- middleman.aiのAPIを使用してPowerPointスライドの自動生成

## 必要条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:
```bash
git clone [repository-url]
cd examples/web_page_to_slide
```

2. 環境変数の設定:
```bash
cp .env.sample .env
```
`.env`ファイルを編集し、必要なAPI keyを設定してください。

3. 依存関係のインストール:
```bash
uv sync
```

## 使用方法

1. langgraphサーバーの起動:
```bash
uv run langgraph run dev
```

2. スライド生成の実行:
```bash
uv run python -m src.web_page_to_slide.agent
```

生成されたスライドはエージェントからの出力として表示されます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
