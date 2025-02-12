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
1) json-to-pptx-analyze: PPTXテンプレートの構造を解析します。
2) json-to-pptx-execute: JSONからPPTXを生成します。

あなたの役割：
1. ユーザーからの依頼に応える返答をJSON形式で生成する
2. json-to-pptx-analyzeで利用するテンプレートの構造を解析する
3. json-to-pptx-analyzeの解析結果に基づいてJSONを生成する
4. json-to-pptx-executeでJSONをPPTXに変換する
5. 生成されたPPTXのURLを返す

最終的な出力は必ずPPTXのURLを含めてください。
""".strip()


middleman_client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))
template_id = os.getenv("MIDDLEMAN_TEMPLATE_ID", "")
analyze_tool = JsonToPptxAnalyzeTool(
    client=middleman_client,
    default_template_id=template_id,
)
execute_tool = JsonToPptxExecuteTool(
    client=middleman_client,
    default_template_id=template_id,
)
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
input = """
以下の説明をもとにmiddlemanについてスライドにまとめて。

# middleman
データを変革しAIを強化する

## 概要
middlemanはあらゆるデータを変換し
現実とAI、AIと現実との橋渡しを行います

## 特徴
### 文書変換の自動化
PDFや業務文書を、AIが理解できる形式に自動変換

### 柔軟な出力対応
AIからの出力を、Word/PowerPoint/Excelなど実務で使える形式に変換

### ローコードでの連携
DifyやGPTsとの連携で、複雑な開発なしでドキュメント変換を実装可能

## middleman.aiの活用シーン
- AIエージェントが収集した情報のレポートをスライド形式やドキュメント形式で出力
- 様々なプロダクトの紹介資料をスプレッドシートやスライドの混合形式で出力
- 学術論文を分かりやすいスライドの形に変換
""".strip()
result = agent_executor.invoke(
    {"input": input},
)
print(result)
