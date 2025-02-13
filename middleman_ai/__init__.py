"""Middleman.ai Python SDK。

このパッケージは、Middleman.aiのAPIを簡単に利用するためのPython SDKを提供します。
主な機能：
- Markdown → PDF変換
- Markdown → DOCX変換
- Markdown → PPTX変換
- PDF → ページ画像変換
- JSON → PPTX変換（テンプレート解析・実行）
"""

from importlib.metadata import version

from .client import ToolsClient
from .exceptions import (
    ConnectionError,
    ForbiddenError,
    InternalError,
    MiddlemanBaseException,
    NotEnoughCreditError,
    NotFoundError,
    ValidationError,
)

__version__ = version(__package__)
__all__ = [
    "ConnectionError",
    "ForbiddenError",
    "InternalError",
    "MiddlemanBaseException",
    "NotEnoughCreditError",
    "NotFoundError",
    "ToolsClient",
    "ValidationError",
]
