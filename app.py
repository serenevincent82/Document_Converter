import os
import tempfile
import zipfile
from pathlib import Path
import streamlit as st
from web_engines import ALL_SUPPORTED_EXTS, convert_web_file

st.set_page_config(page_title="Universal File Converter", page_icon="📄", layout="centered")

st.title("📄 Universal File Converter")
st.write("Convert documents, spreadsheets, presentations, e-books, and images into multiple formats for free.")

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
