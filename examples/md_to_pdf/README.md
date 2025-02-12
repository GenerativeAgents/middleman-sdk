# Markdown to PDF Agent

ユーザーから依頼された内容をMarkdown形式に整形し、PDFに変換するエージェントのサンプルです。

## 機能

- テキスト入力のMarkdown形式への整形
- LLMを使用したコンテンツの最適化
- Middleman.aiのAPIを使用したPDF生成
- 日本語テキストの完全サポート

## 必要条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:
```bash
git clone [repository-url]
cd examples/md_to_pdf
```

2. 環境変数の設定:
```bash
cp .env.sample .env
```
`.env`ファイルを編集し、必要なAPI keyを設定してください：
- `MIDDLEMAN_API_KEY`: Middleman.aiのAPIキー
- `ANTHROPIC_API_KEY`: AnthropicのAPIキー

3. 依存関係のインストール:
```bash
uv sync
```

## 使用方法

1. サンプルスクリプトの実行:
```bash
python -m src.md_to_pdf.agent
```

生成されたPDFのURLがエージェントからの出力として表示されます。

## カスタマイズ

エージェントは以下の方法でカスタマイズ可能です：

```python
from md_to_pdf.agent import process_text_to_pdf

# カスタムテキストの処理
custom_text = """
# カスタムドキュメント
これは**カスタム**コンテンツです。
"""

result = process_text_to_pdf(custom_text)
print(f"生成されたPDF: {result}")
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
