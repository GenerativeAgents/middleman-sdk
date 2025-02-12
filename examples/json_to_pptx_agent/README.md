# JSON to PPTX Agent

ユーザーから依頼された内容をJSON形式に整形し、テンプレートを使用してPPTXに変換するエージェントのサンプルです。

## 機能

- テキスト入力のJSON形式への整形
- LLMを使用したコンテンツの最適化
- Middleman.aiのAPIを使用したPPTX生成
- 日本語テキストの完全サポート
- テンプレートベースのプレゼンテーション生成
- 複雑なレイアウトのサポート
- プレースホルダーの自動マッピング

## 必要条件

- Python 3.10以上
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
python -m src.json_to_pptx_agent.agent
```

生成されたPPTXのURLがエージェントからの出力として表示されます。

## カスタマイズ

エージェントは以下の方法でカスタマイズ可能です：

```python
from json_to_pptx_agent.agent import process_text_to_pptx

# カスタムテキストの処理（テンプレートIDの指定も可能）
custom_text = """
タイトル: プロジェクト計画書

概要スライド:
- プロジェクトの目的
- 実施期間
- 主要マイルストーン

詳細スライド:
1. 実施体制
2. スケジュール
3. 予算計画
"""

result = process_text_to_pptx(custom_text, template_id="your-template-id")
print(f"生成されたPPTX: {result}")
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
