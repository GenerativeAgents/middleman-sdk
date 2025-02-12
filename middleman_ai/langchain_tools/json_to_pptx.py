"""LangChainのJSON to PPTX変換ツール。"""

from typing import Any, List

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, ValidationError

from middleman_ai.client import Presentation, ToolsClient


class JsonToPptxAnalyzeInput(BaseModel):
    """PPTXテンプレート解析用の入力スキーマ。"""

    template_id: str | None = Field(
        None,
        description="PPTXテンプレートのID（UUID形式）。テンプレートの構造を解析するために使用します。省略した場合はデフォルトのテンプレートが利用されます。ユーザーからテンプレートIDの共有がない場合は省略してください。",
    )


class JsonToPptxExecuteInput(BaseModel):
    """PPTXファイル生成用の入力スキーマ。"""

    template_id: str | None = Field(
        None,
        description="PPTXテンプレートのID（UUID形式）。プレゼンテーションの生成に使用します。省略した場合はデフォルトのテンプレートが利用されます。ユーザーからテンプレートIDの共有がない場合は省略してください。",
    )
    presentation: str = Field(
        ...,
        description=f"プレゼンテーションの内容を表すJSON文字列。各スライドのプレースホルダーに挿入するテキストやイメージを以下のJSONスキーマに従って指定します:\n{Presentation.model_json_schema()}",
    )


class JsonToPptxAnalyzeTool(BaseTool):
    """PPTXテンプレートを解析するLangChainツール。"""

    name: str = "json-to-pptx-analyze"
    description: str = (
        "PPTXテンプレートの構造を解析します。"
        "入力はテンプレートID（UUID）である必要があります。"
        "出力はテンプレートの構造情報です。"
    )
    args_schema: type[BaseModel] = JsonToPptxAnalyzeInput
    client: ToolsClient = Field(..., exclude=True)
    default_template_id: str | None = Field(..., exclude=True)

    def __init__(
        self,
        client: ToolsClient,
        default_template_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        kwargs["default_template_id"] = default_template_id
        super().__init__(**kwargs)

    def _run(self, template_id: str | None = None) -> str:
        """同期的にPPTXテンプレートを解析します。

        Args:
            template_id: テンプレートID（UUID）

        Returns:
            str: テンプレートの構造情報を文字列化したもの
        """
        template_id_to_use = template_id or self.default_template_id
        if template_id_to_use is None:
            raise ValueError("テンプレートIDが指定されていません")

        result: List[dict] = self.client.json_to_pptx_analyze_v2(template_id_to_use)
        return "\n".join(
            f"Slide{i + 1}: type={slide.get('type', 'Untitled')} description={slide.get('description', 'No description')}"  # noqa: E501
            f"(placeholders: {', '.join(str(p) for p in slide.get('placeholders', []))})"  # noqa: E501
            for i, slide in enumerate(result)
        )

    async def _arun(
        self,
        template_id: str | None = None,
    ) -> str:
        """非同期的にPPTXテンプレートを解析します。

        Args:
            template_id: テンプレートID（UUID）

        Returns:
            str: テンプレートの構造情報を文字列化したもの
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(template_id)


class JsonToPptxExecuteTool(BaseTool):
    """JSONからPPTXを生成するLangChainツール。"""

    name: str = "json-to-pptx-execute"
    description: str = (
        "テンプレートIDとプレゼンテーションJSONを指定し、PPTXを生成します。"
        "入力は「テンプレートID,JSON」の形式である必要があります（カンマ区切り）。"
        "出力は生成されたPPTXのURLです。"
    )
    args_schema: type[BaseModel] = JsonToPptxExecuteInput
    client: ToolsClient = Field(..., exclude=True)
    default_template_id: str | None = Field(..., exclude=True)

    def __init__(
        self,
        client: ToolsClient,
        default_template_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        kwargs["default_template_id"] = default_template_id
        super().__init__(**kwargs)

    def _run(
        self,
        presentation: str,
        template_id: str | None = None,
    ) -> str:
        """同期的にJSONからPPTXを生成します。

        Args:
            presentation: プレゼンテーションの内容をJSONで表した文字列
            template_id: テンプレートID（UUID）

        Returns:
            str: 生成されたPPTXのURL

        Raises:
            ValueError: 入力形式が不正な場合
            json.JSONDecodeError: JSON形式が不正な場合
        """
        import json

        template_id_to_use = template_id or self.default_template_id
        if template_id_to_use is None:
            raise ValueError("テンプレートIDが指定されていません")

        try:
            presentation_dict = Presentation.model_validate_json(presentation)
        except json.JSONDecodeError as e:
            raise ValueError("不正なJSON形式です") from e
        except ValidationError as e:
            raise ValueError("不正なJSON形式です") from e

        return self.client.json_to_pptx_execute_v2(
            template_id_to_use,
            presentation_dict,
        )

    async def _arun(
        self,
        presentation: str,
        template_id: str | None = None,
    ) -> str:
        """非同期的にJSONからPPTXを生成します。

        Args:
            presentation: プレゼンテーションの内容をJSONで表した文字列
            template_id: テンプレートID（UUID）

        Returns:
            str: 生成されたPPTXのURL
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(presentation, template_id)
