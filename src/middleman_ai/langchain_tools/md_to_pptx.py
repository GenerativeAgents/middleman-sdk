"""LangChainのMarkdown to PPTX変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient

MARKDOWN_GUIDE = """
# マークダウンの書き方ガイド
このツールで扱うマークダウンは作りたいスライドの種類に応じて以下のように記載します。

## タイトルスライド
見出し1を使うことでタイトルスライドが作成できます。

```markdown
## タイトルをここに入れる
```

## セクションスライド
見出し2を使うことでセクションスライドが作成できます。

```markdown
## セクション1
```

## 箇条書きスライド
見出し3の中に「*」を使ってリストを記載することでを利用することで箇条書きスライドを作成できます。
主要なポイントや概要を箇条書きで示すのに適しています。サブ項目（ネストしたリスト）も同様の記法で追加でき、複数階層の箇条書きもサポートされます。

例
```markdown
### 重要なポイント
* ポイント1
* ポイント2
  * サブポイント2.1
  * サブポイント2.2
* ポイント3
```

## 番号付きリストスライド
見出し3と番号付きリストを利用することで、手順や順位付けされた情報を示すスライドを作成できます。Markdownの自動番号付けにより、リストの順序を自由に変更できます。

例
```markdown
### 手順
1. システムを初期化します。
2. 設定を読み込みます。
3. メインルーチンを実行します。
4. 終了します。
```

## テーブルスライド
見出し3とMarkdownのテーブル記法を用いて、データや情報を表形式で整理して表示するスライドを作成できます。
列の見出しと内容は | で区切ります。
2行目のハイフン（-）とコロン（:）の位置で、各列の配置を指定できます：

- 指定なし・左揃え: `-----|` または `:-----|`
- 中央揃え: `:---:|`
- 右揃え: `----:|`

例
```markdown
### データ概要

| 項目       | 左揃え | 中央揃え | 右揃え |
|------------|:-------|:--------:|-------:|
| 例1       | 左     | 中央     | 右     |
| 例2       | 左     | 中央     | 右     |
```
"""


class MdToPptxInput(BaseModel):
    """Markdown to PPTX変換用の入力スキーマ。"""

    text: str = Field(
        ...,
        description="変換対象のMarkdown文字列。以下のガイドに従った有効なMarkdown形式である必要があります。\n"
        + MARKDOWN_GUIDE,
    )


class MdToPptxTool(BaseTool):
    """Markdown文字列をPPTXに変換するLangChainツール。"""

    name: str = "md-to-pptx"
    description: str = (
        "Markdown文字列をPPTXに変換します。"
        "入力は有効なMarkdown文字列である必要があります。"
        "出力は生成されたPPTXのURLです。"
    )
    args_schema: type[BaseModel] = MdToPptxInput
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, text: str) -> str:
        """同期的にMarkdown文字列をPPTXに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPPTXのURL
        """
        return self.client.md_to_pptx(text)

    async def _arun(self, text: str) -> str:
        """非同期的にMarkdown文字列をPPTXに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPPTXのURL
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(text)
