import streamlit as st
import base64
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="学習用PDFビューア", layout="wide")

st.title("📖 学習用PDFビューア")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

if uploaded_file is not None:
    # PDFデータを読み込む
    pdf_reader = PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)

    # ページ選択
    page_number = st.number_input("表示するページ番号を選択", min_value=1, max_value=num_pages, value=1)

    # ページ内容をテキスト化（検索用）
    page_text = pdf_reader.pages[page_number - 1].extract_text()

    # 検索キーワード
    keyword = st.text_input("🔍 PDF内検索（キーワードを入力）")

    # 検索結果のハイライト表示
    if keyword:
        highlighted_text = page_text.replace(keyword, f"**:red[{keyword}]**")
    else:
        highlighted_text = page_text

    st.markdown("### 📄 ページ内容（テキスト表示）")
    st.markdown(highlighted_text)

    # PDF全体をbase64に変換してiframeで表示
    base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" height="800" type="application/pdf">
        </iframe>
    '''
    st.markdown("### 🖼 PDFプレビュー")
    st.markdown(pdf_display, unsafe_allow_html=True)

    # ダウンロードボタン
    st.download_button(
        label="💾 PDFをダウンロード",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="application/pdf"
    )

else:
    st.info("👆 PDFファイルをアップロードすると内容が表示されます。")
