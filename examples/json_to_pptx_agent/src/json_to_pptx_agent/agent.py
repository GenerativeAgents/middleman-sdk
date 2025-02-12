"""JSON to PPTX変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをJSON形式に整形し、
PPTXテンプレートを使用してプレゼンテーションを生成するエージェントを提供します。
すべての処理を1つのファイルにまとめています。
"""

import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.json_to_pptx import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
)

# 環境変数の読み込み
load_dotenv()

# プロンプトの定義
AGENT_PROMPT = """あなたはテキストをPPTXに変換するAIアシスタントです。

以下のツールが利用可能です：
1) json-to-pptx-analyze: PPTXテンプレートの構造を解析します。入力はテンプレートID（省略可）です。出力はテンプレートの構造情報です。
2) json-to-pptx-execute: JSONからPPTXを生成します。入力はスライドの内容を表すJSONとテンプレートID（省略可）です。出力は生成されたPPTXのURLです。

あなたの役割：
1. テンプレートの構造を解析する
2. ユーザーから受け取ったテキストをテンプレートに合わせてJSON形式に整形する
3. 整形したJSONを使用してPPTXを生成する
4. 生成されたPPTXのURLを返す

注意点：
- テンプレートの構造に従ってJSONを生成してください
- プレゼンテーションに適した内容を心がけてください
- 各スライドは簡潔で分かりやすい内容にしてください
- 日本語テキストが適切に処理されることを確認してください
- エラーが発生した場合は、適切なエラーメッセージを返してください

最終的な出力は必ずPPTXのURLを含めてください。"""

def process_text_to_pptx(text: str, template_id: str | None = None) -> Dict[str, Any]:
    """テキストをPPTXに変換します。

    Args:
        text: 変換対象のテキスト
        template_id: テンプレートID（省略可）

    Returns:
        Dict[str, Any]: 処理結果（PPTXのURL等）

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
    analyze_tool = JsonToPptxAnalyzeTool(
        client=middleman_client,
        default_template_id=template_id,
    )
    execute_tool = JsonToPptxExecuteTool(
        client=middleman_client,
        default_template_id=template_id,
    )
    tools = [analyze_tool, execute_tool]

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
    # サンプルテキスト（プレゼンテーション向け）
    sample_text = """
    タイトル: 2024年度 事業計画

    概要スライド:
    - 2023年度の振り返り
    - 2024年度の目標
    - 重点施策

    詳細スライド1 - 2023年度実績:
    - 売上高: 前年比120%
    - 営業利益: 15%増
    - 新規顧客: 50社獲得
    - 主要プロジェクト完遂率: 95%

    詳細スライド2 - 2024年度目標:
    - 売上高目標: 150億円
    - 営業利益目標: 20%増
    - 新規事業開発: 3件
    - 顧客満足度: 90%以上

    詳細スライド3 - 重点施策:
    1. デジタル化推進
       - 社内システムの刷新
       - 業務プロセスの自動化
    2. 人材育成
       - 研修プログラムの拡充
       - グローバル人材の育成
    3. 新規事業展開
       - AI関連事業の強化
       - 海外市場への進出

    まとめスライド:
    - 2024年度は積極的な投資と成長の年
    - デジタル化と人材育成に注力
    - 持続可能な成長を目指す
    """

    try:
        result = process_text_to_pptx(sample_text)
        print("=== PPTX生成結果 ===")
        print(f"生成されたPPTX: {result}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
