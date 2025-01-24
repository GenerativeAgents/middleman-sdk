"""Middleman.ai SDKの例外クラスを定義するモジュール。"""

from typing import Optional


class MiddlemanBaseException(Exception):
    """全てのSDK固有例外の親クラス。"""

    def __init__(self, message: Optional[str] = None) -> None:
        """例外を初期化します。

        Args:
            message: エラーメッセージ
        """
        super().__init__(message or self.__class__.__doc__ or "An error occurred")


class NotEnoughCreditError(MiddlemanBaseException):
    """クレジット不足によりAPIの実行ができません。"""


class ForbiddenError(MiddlemanBaseException):
    """APIキーが無効か、アクセス権限がありません。"""


class NotFoundError(MiddlemanBaseException):
    """要求されたリソースが見つかりません。"""


class InternalError(MiddlemanBaseException):
    """サーバー内部でエラーが発生しました。"""


class ConnectionError(MiddlemanBaseException):
    """APIサーバーとの接続に失敗しました。"""


class ValidationError(MiddlemanBaseException):
    """入力データのバリデーションに失敗しました。"""
