import streamlit as st
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="📖 学習用PDFビューア", layout="wide")

st.title("📖 学習用PDFビューア（安全版）")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

if uploaded_file is not None:
    # PDFを読み込む
    pdf_reader = PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)

    # ページ番号選択
    page_number = st.number_input(
        "📄 表示するページ番号",
        min_value=1,
        max_value=num_pages,
        value=1,
    )

    # ページのテキストを抽出
    page = pdf_reader.pages[page_number - 1]
    text = page.extract_text() or "(このページには抽出できるテキストがありません)"

    # 検索ボックス
    keyword = st.text_input("🔍 テキスト検索（キーワードを入力）")

    # ハイライト処理
    if keyword:
        highlighted = text.replace(keyword, f"**:red[{keyword}]**")
    else:
        highlighted = text

    # テキストを表示
    st.markdown("### 📘 ページの内容（テキスト抽出）")
    st.markdown(highlighted)

    # PDFをネイティブ表示（Chromeでもブロックされない）
    st.markdown("### 🖼 PDFプレビュー")
    st.pdf(uploaded_file)

    # ダウンロードボタン
    st.download_button(
        label="💾 PDFをダウンロード",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="application/pdf",
    )
else:
    st.info("👆 上のボタンからPDFファイルを選択してください。")
