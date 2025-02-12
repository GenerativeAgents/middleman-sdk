# Markdown to DOCX Agent

ユーザーから依頼された内容をMarkdown形式に整形し、DOCXに変換するエージェントのサンプルです。

## 機能

- テキスト入力のMarkdown形式への整形
- LLMを使用したコンテンツの最適化
- Middleman.aiのAPIを使用したDOCX生成
- 日本語テキストの完全サポート
- ビジネス文書向けの最適化

## 必要条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:
```bash
git clone [repository-url]
cd examples/md_to_docx_agent
```

2. 環境変数の設定:
```bash
cp .env.sample .env
```
`.env`ファイルを編集し、必要なAPI keyを設定してください：
- `MIDDLEMAN_API_KEY`: Middleman.aiのAPIキー
- `OPENAI_API_KEY`: OpenAIのAPIキー

3. 依存関係のインストール:
```bash
uv sync
```

## 使用方法

1. サンプルスクリプトの実行:
```bash
python -m src.md_to_docx_agent.agent
```

生成されたDOCXのURLがエージェントからの出力として表示されます。

## カスタマイズ

エージェントは以下の方法でカスタマイズ可能です：

```python
from md_to_docx_agent.agent import process_text_to_docx

# カスタムテキストの処理
custom_text = """
# ビジネスレポート
これは**重要な**ビジネス文書です。
"""

result = process_text_to_docx(custom_text)
print(f"生成されたDOCX: {result}")
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
