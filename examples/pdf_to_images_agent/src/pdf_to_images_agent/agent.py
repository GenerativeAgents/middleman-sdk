"""PDFをページごとの画像に変換するエージェントの実装。"""

import os
from typing import List

from dotenv import load_dotenv
from langchain_core.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.pdf_to_page_images import PdfToPageImagesTool

load_dotenv()

def create_agent(
    *,
    client: ToolsClient,
    model: str = "gpt-4",
) -> AgentExecutor:
    """PDFをページごとの画像に変換するエージェントを作成します。

    Args:
        client: Middleman.ai APIクライアント
        model: 使用するLLMのモデル名

    Returns:
        AgentExecutor: 設定済みのエージェント
    """
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=model,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

    tools: List[PdfToPageImagesTool] = [
        PdfToPageImagesTool(client=client),
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたはPDFファイルをページごとの画像に変換するアシスタントです。"
                  "ユーザーから受け取ったPDFファイルパスを使用して、各ページを画像に変換します。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = AgentExecutor.from_agent_and_tools(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        prompt=prompt,
        verbose=True,
    )

    return agent
