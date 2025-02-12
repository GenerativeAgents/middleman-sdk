import json
import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledGraph
from langgraph.prebuilt import create_react_agent

from middleman_ai.client import Presentation, ToolsClient

load_dotenv()


def load_prompt(prompt_name: str) -> str:
    """Load a prompt file from the prompts directory.

    Args:
        prompt_name: Name of the prompt file (without .txt extension)

    Returns:
        str: Content of the prompt file

    Raises:
        FileNotFoundError: If the prompt file is not found
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "prompts", f"{prompt_name}.txt")

    with open(prompt_path) as f:
        return f.read()


class WebPageAnalysisTool(BaseTool):
    """Tool to fetch web pages and extract text and image URLs from a given URL"""

    name: str = "web-page-analyze"
    description: str = (
        "Fetches a web page from the specified URL and extracts text and image URLs. "
        "Input: Valid URL string. "
        "Output: JSON string {text: str, images: list[str]}."
    )

    def _run(self, url: str) -> str:
        """Fetch a web page and extract text and image URLs from the specified URL.

        Args:
            url: Target URL string

        Returns:
            str: Extracted text and image URLs in JSON format

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        from typing import Any

        import requests
        from bs4 import BeautifulSoup, Tag

        # Get HTML from URL
        resp: Any = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = str(resp.text)

        # Parse HTML and extract text and image URLs
        soup = BeautifulSoup(html, "html.parser")
        text = str(soup.get_text(separator="\n"))
        images = [
            str(tag.get("src", ""))
            for tag in soup.find_all("img")
            if isinstance(tag, Tag)
        ]

        # Return results in JSON format
        result = {"text": text[:2000], "images": images[:10]}
        return json.dumps(result, ensure_ascii=False)

    async def _arun(self, url: str) -> str:
        """Execute asynchronous page analysis.

        Args:
            url: Target URL string

        Returns:
            str: Extracted text and image URLs in JSON format
        """
        return self._run(url)


class TextToSlideJsonTool(BaseTool):
    """Tool to convert text into slide JSON format"""

    name: str = "text-to-slide-json"
    description: str = (
        "Input: Text string that includes content text, source URL, and image URLs with their descriptions. "  # noqa: E501
        "The source URL should be in the format 'Source URL: [URL]'. "
        "The image information should be in the format 'Image URL: [URL], Description: [description]'. "  # noqa: E501
        "Output: JSON string {text: str, images: list[str]}."
    )
    client: ToolsClient
    llm: ChatAnthropic
    template_slide_id: str

    def _run(self, text: str) -> str:
        slide_template_str = self.client.json_to_pptx_analyze_v2(self.template_slide_id)
        prompt = ChatPromptTemplate.from_template(load_prompt("text_to_slide_json"))
        chain = prompt | self.llm.with_structured_output(Presentation)
        result: Presentation = Presentation.model_validate(
            chain.invoke(
                {
                    "content": text,
                    "slide_templates": slide_template_str,
                }
            )
        )
        return json.dumps(result.to_dict(), ensure_ascii=False)


class JsonToPptxExecuteTool(BaseTool):
    """Tool to generate PPTX from JSON"""

    name: str = "json-to-pptx-execute"
    description: str = "Generate PPTX from JSON"
    client: ToolsClient
    template_slide_id: str

    def _run(self, json_str: str) -> str:
        result: str = self.client.json_to_pptx_execute_v2(
            pptx_template_id=self.template_slide_id,
            presentation=Presentation.model_validate(json.loads(json_str)),
        )
        return result


def create_slide_agent(
    template_slide_id: str,
    middleman_api_key: str,
    anthropic_api_key: str,
) -> CompiledGraph:
    """Create a slide generation agent.

    Args:
        template_slide_id: ID of the template slide
        middleman_api_key: API key for Middleman service
        anthropic_api_key: API key for Anthropic service

    Returns:
        CompiledGraph: Compiled agent graph
    """
    middleman_client = ToolsClient(api_key=middleman_api_key)

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=0.0,
        api_key=anthropic_api_key,
    )

    tool_page_get = WebPageAnalysisTool()
    tool_convert_tpl = TextToSlideJsonTool(
        client=middleman_client,
        llm=llm,
        template_slide_id=template_slide_id,
    )
    tool_exec_tpl = JsonToPptxExecuteTool(
        client=middleman_client,
        template_slide_id=template_slide_id,
    )
    tools_list = [tool_page_get, tool_convert_tpl, tool_exec_tpl]

    compiled_graph = create_react_agent(
        model=llm,
        tools=tools_list,
        prompt=load_prompt("agent"),
        checkpointer=MemorySaver(),
    )

    return compiled_graph


agent = create_slide_agent(
    template_slide_id=os.getenv("TEMPLATE_SLIDE_ID") or "",
    middleman_api_key=os.getenv("MIDDLEMAN_API_KEY") or "",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or "",
)

if __name__ == "__main__":
    import uuid

    from langchain_core.runnables import RunnableConfig

    config = RunnableConfig({"configurable": {"thread_id": str(uuid.uuid4())}})

    initial_state = {
        "messages": [
            (
                "human",
                "Please make slides from https://blog.generative-agents.co.jp/entry/2025/01/30/134659",
            )
        ]
    }

    for state in agent.stream(initial_state, stream_mode="values", config=config):
        # Display the last message of each step (State)
        last_msg = state.get("messages", [])[-1]
        print(last_msg)
        print("-----")
        if hasattr(last_msg, "pretty_print"):
            last_msg.pretty_print()
