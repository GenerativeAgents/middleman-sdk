# Markdown to PPTX Agent

ユーザーから依頼された内容をMarkdown形式に整形し、PPTXに変換するエージェントのサンプルです。

## 機能

- テキスト入力のMarkdown形式への整形
- LLMを使用したコンテンツの最適化
- Middleman.aiのAPIを使用したPPTX生成
- 日本語テキストの完全サポート
- プレゼンテーション向けの最適化
- 効果的なスライド構造の自動生成

## 必要条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv)

## セットアップ

1. リポジトリをクローン:
```bash
git clone [repository-url]
cd examples/md_to_pptx_agent
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
python -m src.md_to_pptx_agent.agent
```

生成されたPPTXのURLがエージェントからの出力として表示されます。

## カスタマイズ

エージェントは以下の方法でカスタマイズ可能です：

```python
from md_to_pptx_agent.agent import process_text_to_pptx

# カスタムテキストの処理
custom_text = """
# プレゼンテーションタイトル

## スライド1
- 要点1
- 要点2

## スライド2
1. 項目1
2. 項目2
"""

result = process_text_to_pptx(custom_text)
print(f"生成されたPPTX: {result}")
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
