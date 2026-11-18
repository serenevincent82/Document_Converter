# Universal File Converter

A free, open-source web app built with **Python** and **Streamlit** to batch-convert documents, spreadsheets, presentations, e-books, and images directly in your browser.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://documentconversion.streamlit.app/)

---

## ✨ Key Features
* **Batch & Multi-Format:** Upload multiple files and convert each into several formats at once.
* **ZIP Export:** Downloads all converted files organized into folders inside `converted_output.zip`.
* **Privacy First:** Processes files in temporary directories that wipe automatically after download.

---

## 📂 Supported Formats
Convert between major **Documents** (PDF, DOCX, TXT, MD, HTML), **Spreadsheets** (XLSX, CSV), **Presentations** (PPTX), **Images** (JPG, PNG, TIFF), and **E-Books** (EPUB, MOBI, AZW3, DJVU) — including cross-exports to **PDF** and **DOCX**.

---

## 💻 Quick Start (Local)

**Prerequisites:** Python 3.10+, [LibreOffice](https://www.libreoffice.org/), and [Calibre](https://calibre-ebook.com/) *(optional, for e-books)*.

```bash
pip install -r requirements.txt
streamlit run app.py
