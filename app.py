import os
import tempfile
import zipfile
from pathlib import Path
import streamlit as st
from web_engines import ALL_SUPPORTED_EXTS, convert_web_file

st.set_page_config(page_title="Universal File Converter", page_icon="📄", layout="centered")

# st.title("📄 Universal File Converter")
# st.write("Convert documents, spreadsheets, presentations, e-books, and images into multiple formats for free.")
# # --- CUSTOM DESIGN & STYLING ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* 1. Global Font & Subtle Document-Grid Background */
html, body, [class*="css"], .stMarkdown, p, label, button, input, select {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background-color: #0B0F19;
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.16) 0%, transparent 55%),
        linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 100% 100%, 32px 32px, 32px 32px;
}

/* Hide default Streamlit top bar & footer */
#MainMenu, header, footer { visibility: hidden; }

/* 2. Center & Card-Frame the Main Container */
.block-container {
    max-width: 720px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}

/* 3. Aligned Hero Header */
.hero-box {
    text-align: center;
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #A5B4FC;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}
.hero-sub {
    color: #94A3B8;
    font-size: 1rem;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.5;
}

/* 4. Attractive Upload Dropzone */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(19, 26, 42, 0.85) !important;
    border: 1.5px dashed rgba(99, 102, 241, 0.45) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    transition: all 0.2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #818CF8 !important;
    background: rgba(30, 41, 59, 0.9) !important;
}

/* 5. Format Selector & Primary Button */
.stMultiSelect > div > div {
    background-color: #131A2A !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    border-radius: 10px !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.25rem !important;
    margin-top: 0.5rem !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
}
</style>

<div class="hero-box">
    <div class="hero-badge">📄 FAST & FREE FILE UTILITY</div>
    <h1 class="hero-title">Universal File Converter</h1>
    <p class="hero-sub">Convert documents, spreadsheets, presentations, e-books, and images into multiple formats in seconds.</p>
</div>
""", unsafe_allow_html=True)

FORMAT_OPTIONS = {
    "PDF Document (.pdf)": "pdf",
    "Word Document (.docx)": "docx",
    "Word 97-2003 (.doc)": "doc",
    "OpenDocument Text (.odt)": "odt",
    "Rich Text Format (.rtf)": "rtf",
    "Excel Workbook (.xlsx)": "xlsx",
    "Excel 97-2003 (.xls)": "xls",
    "OpenDocument Spreadsheet (.ods)": "ods",
    "CSV Comma Delimited (.csv)": "csv",
    "PowerPoint Presentation (.pptx)": "pptx",
    "PowerPoint 97-2003 (.ppt)": "ppt",
    "OpenDocument Presentation (.odp)": "odp",
    "JPG Images (.jpg)": "jpg",
    "PNG Images (.png)": "png",
    "TIFF Images (.tiff)": "tiff",
    "Plain Text (.txt)": "txt",
    "Markdown (.md)": "md",
    "HTML Web Page (.html)": "html",
    "XML Data (.xml)": "xml",
    "EPUB E-Book (.epub)": "epub",
    "MOBI E-Book (.mobi)": "mobi",
    "Kindle AZW3 (.azw3)": "azw3",
}

if "zip_bytes" not in st.session_state:
    st.session_state.zip_bytes = None

uploaded_files = st.file_uploader(
    "1. Upload one or more files",
    type=ALL_SUPPORTED_EXTS,
    accept_multiple_files=True,
)

selected_labels = st.multiselect(
    "2. Choose target output format(s)",
    options=list(FORMAT_OPTIONS.keys()),
    default=["PDF Document (.pdf)"],
)

if st.button("Convert Files", type="primary", disabled=not (uploaded_files and selected_labels)):
    target_exts = [FORMAT_OPTIONS[label] for label in selected_labels]
    st.session_state.zip_bytes = None

    with tempfile.TemporaryDirectory() as tmp_root:
        zip_path = os.path.join(tmp_root, "converted_files.zip")
        total_created = 0

        with st.status("Converting your files...", expanded=True) as status:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for idx, uploaded in enumerate(uploaded_files):
                    src_name = uploaded.name
                    src_stem = Path(src_name).stem
                    src_ext = Path(src_name).suffix.lower().lstrip(".")

                    file_work_dir = os.path.join(tmp_root, f"work_{idx}_{src_stem}")
                    os.makedirs(file_work_dir, exist_ok=True)
                    src_path = os.path.join(file_work_dir, src_name)

                    with open(src_path, "wb") as f:
                        f.write(uploaded.getbuffer())

                    st.write(f"**Processing:** `{src_name}`")
                    for t_ext in target_exts:
                        if src_ext == t_ext:
                            st.write(f"⏭️ Skipped `.{t_ext}` (already in this format)")
                            continue

                        fmt_out_dir = os.path.join(file_work_dir, t_ext)
                        os.makedirs(fmt_out_dir, exist_ok=True)

                        try:
                            produced_files = convert_web_file(src_path, t_ext, fmt_out_dir)
                            for prod in produced_files:
                                folder_name = f"{src_stem}_{src_ext}"
                                arcname = os.path.join(folder_name, os.path.basename(prod))
                                zf.write(prod, arcname=arcname)
                                total_created += 1
                            st.write(f"✅ Converted to `.{t_ext}`")
                        except Exception as e:
                            st.error(f"❌ Failed `{src_name}` → `.{t_ext}`: {e}")

            status.update(label=f"Done! Created {total_created} file(s).", state="complete")

        if total_created > 0:
            with open(zip_path, "rb") as zf_bytes:
                st.session_state.zip_bytes = zf_bytes.read()

if st.session_state.zip_bytes:
    st.download_button(
        label="⬇️ Download All Converted Files (.ZIP)",
        data=st.session_state.zip_bytes,
        file_name="converted_output.zip",
        mime="application/zip",
        type="primary",
    )
