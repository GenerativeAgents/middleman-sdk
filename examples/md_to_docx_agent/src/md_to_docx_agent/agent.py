"""Markdown to DOCX変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをMarkdown形式に整形し、
DOCXに変換するエージェントを提供します。すべての処理を1つのファイルにまとめています。
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.md_to_docx import MdToDocxTool

# 環境変数の読み込み
load_dotenv()

# プロンプトの定義
AGENT_PROMPT = """あなたはMarkdownテキストをDOCXに変換するAIアシスタントです。

以下のツールが利用可能です：
1) md-to-docx: Markdown文字列をDOCXに変換します。入力は有効なMarkdown形式である必要があります。出力は生成されたDOCXのURLです。

あなたの役割：
1. ユーザーから受け取ったテキストを適切なMarkdown形式に整形する
2. 整形したMarkdownテキストをDOCXに変換する
3. 生成されたDOCXのURLを返す

注意点：
- Markdownの構文が正しいことを確認してください
- 日本語テキストが適切に処理されることを確認してください
- エラーが発生した場合は、適切なエラーメッセージを返してください
- ビジネス文書に適した形式を心がけてください

最終的な出力は必ずDOCXのURLを含めてください。"""

def process_text_to_docx(text: str) -> Dict[str, Any]:
    """テキストをDOCXに変換します。

    Args:
        text: 変換対象のテキスト

    Returns:
        Dict[str, Any]: 処理結果（DOCXのURL等）

    Raises:
        ValueError: 必要な環境変数が設定されていない場合
    """
    # API keyの取得
    middleman_api_key = os.getenv("MIDDLEMAN_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not middleman_api_key or not openai_api_key:
        raise ValueError(
            "環境変数が設定されていません。"
            "MIDDLEMAN_API_KEY と OPENAI_API_KEY を設定してください。"
        )

    # クライアントの初期化
    middleman_client = ToolsClient(api_key=middleman_api_key)

    # LLMの設定
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0.0,
        api_key=openai_api_key,
    )

    # ツールの設定
    md_to_docx_tool = MdToDocxTool(client=middleman_client)
    tools = [md_to_docx_tool]

    # プロンプトの設定
    prompt = ChatPromptTemplate.from_template(AGENT_PROMPT)

    # エージェントの作成
    agent = AgentExecutor.from_agent_and_tools(
        agent="structured-chat-zero-shot-react-description",
        llm=llm,
        tools=tools,
        verbose=True,
    )

    # テキストの処理
    result = agent.invoke({"input": text})
    return result


if __name__ == "__main__":
    # サンプルテキスト（ビジネス文書向け）
    sample_text = """
    # プロジェクト進捗報告書

    ## プロジェクト概要
    - プロジェクト名: AI文書変換システム開発
    - 期間: 2024年1月 - 2024年3月
    - 担当部署: 技術開発部

    ## 進捗状況
    ### 完了タスク
    1. 要件定義
    2. 基本設計
    3. 詳細設計

    ### 進行中タスク
    - プロトタイプ開発
    - ユニットテスト作成
    - ドキュメント作成

    ## 課題と対策
    | 課題 | 対策 | 状況 |
    |------|------|------|
    | パフォーマンス改善 | キャッシュ機能の実装 | 対応中 |
    | セキュリティ強化 | 認証機能の追加 | 計画済 |

    ## 今後のスケジュール
    1. 4月: 結合テスト
    2. 5月: システムテスト
    3. 6月: ユーザーテスト
    4. 7月: 本番リリース

    ## 添付資料
    詳細な技術仕様については[技術文書](https://example.com/docs)を参照してください。
    """

    try:
        result = process_text_to_docx(sample_text)
        print("=== DOCX生成結果 ===")
        print(f"生成されたDOCX: {result}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
