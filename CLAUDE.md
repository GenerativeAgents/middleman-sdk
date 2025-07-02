# CLAUDE.md

このファイルはこのリポジトリでコードを扱う際のClaude Code (claude.ai/code) へのガイダンスを提供します。

## コマンド

### 開発用コマンド
```bash
# テスト実行
uv run pytest

# リンター実行
uv run ruff check .
uv run mypy ./src

# タイプチェック
uv run mypy ./src

# コードフォーマット
uv run black .
```

### ビルドと配布
詳細は [README-for-developer.md](README-for-developer.md) の「配布」セクションを参照してください。

### CLIテスト
```bash
# APIキー設定
export MIDDLEMAN_API_KEY=your-api-key

# CLIコマンドテスト
echo "# テスト" | uvx middleman md-to-pdf [template-id]
uvx middleman pdf-to-page-images input.pdf
```

## アーキテクチャ

Middleman.ai API用のPython SDKで、3つの主要なインターフェース層から構成されています：

### 1. コアクライアント (`src/middleman_ai/client.py`)
- `ToolsClient`: HTTPセッション管理を含むメインAPIクライアントクラス
- 全APIエンドポイント実装: `md_to_pdf`, `md_to_docx`, `pdf_to_page_images`など
- `exceptions.py`でカスタム例外による集約エラーハンドリング
- `models.py`でPydanticモデルとしてレスポンス定義

### 2. LangChainツール (`src/middleman_ai/langchain_tools/`)
- 各ツールはLangChainの`BaseTool`を継承
- AIエージェント用にクライアントメソッドをラップ
- `_run`と`_arun`メソッド両方を実装
- ツール例: `MdToPdfTool`, `JsonToPptxAnalyzeTool`など

### 3. MCPサーバー (`src/middleman_ai/mcp/server.py`)
- FastMCPを使用したModel Context Protocol実装
- Claude Desktopやその他MCPクライアントにツールを公開
- `@mcp.tool()`デコレータによる自動登録
- テキスト入力とファイルパス入力の両方をサポート

### 4. CLIインターフェース (`src/middleman_ai/cli/main.py`)
- Clickベースのコマンドラインインターフェース
- 標準入力またはファイル引数からの読み込み
- 環境変数設定 (`MIDDLEMAN_API_KEY`, `MIDDLEMAN_BASE_URL`)

## テスト戦略

### 単体テスト (`tests/test_*.py`)
- pytest-mockを使用してHTTPリクエストをモック
- API呼び出しなしでクライアントロジックをテスト
- 成功/エラーシナリオとパラメータ検証をカバー

### VCRテスト (`tests/test_*_vcr.py`)
- VCR.pyカセットを使用した実際のAPI統合テスト
- 環境に依存しないアサーション（正確な値ではなくURLパターンをチェック）
- テンプレートIDや機密データには環境変数を使用

### テストデータ
- `tests/data/`にサンプルファイル
- `tests/cassettes/`にVCRカセット
- `vcr_utils.py`にテストユーティリティ

## 主要な実装ルール

### エラーハンドリング
- クライアントで集約例外ハンドリングを使用
- HTTPステータスコードを特定の例外タイプにマップ
- 適切なエラー伝播でPydanticレスポンスを解析

### コードスタイル
- Blackフォーマット（行長: 88）
- 特定のルールセットでRuffリンティング
- 型ヒント必須（mypyで強制）
- 全API リクエスト/レスポンスデータにPydanticモデル

### 環境設定
- `MIDDLEMAN_API_KEY`: API認証に必須
- `MIDDLEMAN_BASE_URL`: APIベースURL（デフォルトは本番環境）
- VCRテストでテンプレートID用のテスト環境変数