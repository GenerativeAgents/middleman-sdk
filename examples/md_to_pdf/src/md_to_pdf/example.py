"""サンプルスクリプト。

このスクリプトは、Markdown to PDFエージェントの使用例を示します。
"""

from md_to_pdf.agent import process_text_to_pdf


def main() -> None:
    """サンプルテキストを使用してPDF生成を実行します。"""
    sample_text = """
    # ビジネスレポート

    ## 概要
    このレポートは、2024年第1四半期の業績をまとめたものです。

    ## 主要な成果
    - 売上高: 前年比120%
    - 新規顧客: 50社
    - 顧客満足度: 95%

    ## 今後の展望
    1. グローバル展開の加速
    2. 新製品の開発
    3. 顧客サービスの向上

    ## 結論
    第1四半期は好調な結果となりました。
    """

    try:
        result = process_text_to_pdf(sample_text)
        print("=== PDF生成結果 ===")
        print(f"生成されたPDF: {result}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
