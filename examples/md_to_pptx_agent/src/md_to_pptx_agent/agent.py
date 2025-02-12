"""Markdown to PPTX変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをMarkdown形式に整形し、
PPTXに変換するエージェントを提供します。すべての処理を1つのファイルにまとめています。
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.md_to_pptx import MdToPptxTool

# 環境変数の読み込み
load_dotenv()

# プロンプトの定義
AGENT_PROMPT = """あなたはMarkdownテキストをPPTXに変換するAIアシスタントです。

以下のツールが利用可能です：
1) md-to-pptx: Markdown文字列をPPTXに変換します。入力は有効なMarkdown形式である必要があります。出力は生成されたPPTXのURLです。

あなたの役割：
1. ユーザーから受け取ったテキストを適切なMarkdown形式に整形する
2. 整形したMarkdownテキストをPPTXに変換する
3. 生成されたPPTXのURLを返す

注意点：
- Markdownの構文が正しいことを確認してください
- プレゼンテーションに適した構造を心がけてください
- 各スライドは簡潔で分かりやすい内容にしてください
- 箇条書きや見出しを効果的に使用してください
- 日本語テキストが適切に処理されることを確認してください
- エラーが発生した場合は、適切なエラーメッセージを返してください

最終的な出力は必ずPPTXのURLを含めてください。"""

def process_text_to_pptx(text: str) -> Dict[str, Any]:
    """テキストをPPTXに変換します。

    Args:
        text: 変換対象のテキスト

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
    md_to_pptx_tool = MdToPptxTool(client=middleman_client)
    tools = [md_to_pptx_tool]

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
    # AI技術の最新動向

    ## はじめに
    - AI技術は急速に進化しています
    - 様々な分野で革新的な応用が進んでいます

    ## 主要なトレンド
    ### 生成AI
    - 大規模言語モデル
    - 画像生成AI
    - 音声合成技術

    ### 自動化技術
    - RPA（ロボティック・プロセス・オートメーション）
    - ワークフロー自動化
    - 予測分析

    ## 産業への影響
    1. 製造業
       - 品質管理の自動化
       - 予知保全の実現
    2. 金融業
       - リスク分析の高度化
       - 不正検知の強化
    3. 医療分野
       - 診断支援
       - 創薬研究の効率化

    ## 今後の展望
    - さらなる技術革新
    - 社会実装の加速
    - 倫理的課題への対応

    ## まとめ
    AIは私たちの生活や産業を大きく変革する可能性を秘めています。
    """

    try:
        result = process_text_to_pptx(sample_text)
        print("=== PPTX生成結果 ===")
        print(f"生成されたPPTX: {result}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
