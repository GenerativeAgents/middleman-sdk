"""Markdown to PDF変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをMarkdown形式に整形し、
PDFに変換するエージェントを提供します。
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.md_to_pdf import MdToPdfTool

load_dotenv()


def load_prompt(prompt_name: str) -> str:
    """プロンプトファイルを読み込みます。

    Args:
        prompt_name: プロンプトファイル名（.txt拡張子なし）

    Returns:
        str: プロンプトファイルの内容

    Raises:
        FileNotFoundError: プロンプトファイルが見つからない場合
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "prompts", f"{prompt_name}.txt")

    with open(prompt_path) as f:
        return f.read()


def create_pdf_agent(
    middleman_api_key: str,
    anthropic_api_key: str,
) -> AgentExecutor:
    """PDF生成エージェントを作成します。

    Args:
        middleman_api_key: Middleman.aiのAPIキー
        anthropic_api_key: AnthropicのAPIキー

    Returns:
        AgentExecutor: 設定済みのエージェント
    """
    middleman_client = ToolsClient(api_key=middleman_api_key)

    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0.0,
        api_key=anthropic_api_key,
    )

    md_to_pdf_tool = MdToPdfTool(client=middleman_client)
    tools = [md_to_pdf_tool]

    prompt = ChatPromptTemplate.from_template(load_prompt("agent"))

    agent = AgentExecutor.from_agent_and_tools(
        agent="structured-chat-zero-shot-react-description",
        llm=llm,
        tools=tools,
        verbose=True,
    )

    return agent


def process_text_to_pdf(text: str) -> Dict[str, Any]:
    """テキストをPDFに変換します。

    Args:
        text: 変換対象のテキスト

    Returns:
        Dict[str, Any]: 処理結果（PDFのURL等）

    Raises:
        ValueError: 必要な環境変数が設定されていない場合
    """
    middleman_api_key = os.getenv("MIDDLEMAN_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if not middleman_api_key or not anthropic_api_key:
        raise ValueError(
            "環境変数が設定されていません。"
            "MIDDLEMAN_API_KEY と ANTHROPIC_API_KEY を設定してください。"
        )

    agent = create_pdf_agent(
        middleman_api_key=middleman_api_key,
        anthropic_api_key=anthropic_api_key,
    )

    result = agent.invoke({"input": text})
    return result


if __name__ == "__main__":
    sample_text = """
    # サンプルドキュメント

    これはサンプルのMarkdownドキュメントです。

    ## 特徴
    - シンプルな構造
    - 日本語対応
    - Markdown形式

    詳細については[Markdown Guide](https://www.markdownguide.org)を参照してください。
    """

    try:
        result = process_text_to_pdf(sample_text)
        print("生成されたPDF:", result)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
