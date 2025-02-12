"""Markdown to PPTX変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをMarkdown形式に整形し、
PPTXに変換するエージェントを提供します。
"""

import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.md_to_pptx import MdToPptxTool

load_dotenv()


SYSTEM_PROMPT = """
あなたはMarkdownテキストをPPTXに変換するAIアシスタントです。

以下のツールが利用可能です：
1) md-to-pptx: Markdown文字列をPPTXに変換します。

あなたの役割：
1. ユーザーからの依頼に応える返答をMarkdown形式で生成する
2. 整形したMarkdownテキストをPPTXに変換する
3. 生成されたPPTXのURLを返す

最終的な出力は必ずPPTXのURLを含めてください。
""".strip()


middleman_client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))
md_to_pptx_tool = MdToPptxTool(client=middleman_client)
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
)
tools = [md_to_pptx_tool]
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=False,
)
input = """
AI技術の最新トレンドについて多角的な観点でまとめたPPTX資料を作成して
""".strip()
result = agent_executor.invoke(
    {"input": input,},
)
print(result)
