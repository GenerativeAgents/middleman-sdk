"""JSON to PPTX変換エージェント。

このモジュールは、ユーザーから受け取ったテキストをJSON形式に整形し、
PPTXに変換するエージェントを提供します。
"""

import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools.json_to_pptx import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
)

load_dotenv()


SYSTEM_PROMPT = """
あなたはテキストをPPTXに変換するAIアシスタントです。

以下のツールが利用可能です：
1) json-to-pptx-analyze: PPTXテンプレートの構造を解析します。テンプレートIDは省略可能です。
2) json-to-pptx-execute: JSONからPPTXを生成します。テンプレートIDは省略可能です。

あなたの役割：
1. ユーザーからの依頼に応える返答をJSON形式で生成する
2. テンプレートの構造を解析する
3. 解析結果に基づいてJSONを生成し、PPTXに変換する
4. 生成されたPPTXのURLを返す

最終的な出力は必ずPPTXのURLを含めてください。
""".strip()


middleman_client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))
analyze_tool = JsonToPptxAnalyzeTool(client=middleman_client)
execute_tool = JsonToPptxExecuteTool(client=middleman_client)
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
)
tools = [analyze_tool, execute_tool]
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
result = agent_executor.invoke({"input": "2024年度の事業計画についてプレゼン資料を作成して"})
print(result)
