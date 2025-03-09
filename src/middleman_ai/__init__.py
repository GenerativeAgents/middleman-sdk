"""Middleman.ai Python SDK。

このパッケージは、Middleman.aiのAPIを簡単に利用するためのPython SDKを提供します。
主な機能：
- Markdown → PDF変換
- Markdown → DOCX変換
- Markdown → PPTX変換
- PDF → ページ画像変換
- JSON → PPTX変換（テンプレート解析・実行）
"""

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

try:
    from importlib.metadata import version

    __version__ = version("middleman-ai")
except ImportError:
    __version__ = "unknown"
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
