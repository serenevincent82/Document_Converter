# 📄 Universal File Converter (Web App)

A free, open-source web application built with **Python** and **Streamlit** that converts documents, spreadsheets, presentations, e-books, web files, and images into multiple formats directly in your browser.

---

## ✨ Features
* **Multi-File Batch Upload:** Upload one or multiple files at the same time via drag-and-drop.
* **Multi-Format Conversion:** Convert each uploaded file into one or several target formats simultaneously.
* **Organized ZIP Download:** Automatically bundles all converted outputs into clean, file-named folders inside a single `converted_output.zip` download.
* **Zero HTML/CSS Required:** Built purely in Python using Streamlit's interactive web interface.
* **100% Free Hosting:** Ready for instant, zero-cost deployment on Streamlit Community Cloud.

---

## 📂 Supported Formats

| Category | Supported Input Formats | Supported Output Formats |
| :--- | :--- | :--- |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.odt`, `.rtf`, `.txt`, `.md`, `.html`, `.xml`, `.xps` | `.pdf`, `.docx`, `.doc`, `.odt`, `.rtf`, `.txt`, `.md`, `.html`, `.xml` |
| **Spreadsheets** | `.xls`, `.xlsx`, `.ods`, `.csv` | `.xlsx`, `.xls`, `.ods`, `.csv`, `.pdf` |
| **Presentations** | `.ppt`, `.pptx`, `.odp` | `.pptx`, `.ppt`, `.odp`, `.pdf` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.tiff` | `.jpg`, `.png`, `.tiff`, `.pdf`, `.docx` |
| **E-Books & DjVu** | `.epub`, `.mobi`, `.azw3`, `.djvu` | `.epub`, `.mobi`, `.azw3`, `.pdf`, `.txt`, `.html` |

---

## 🛠️ Project Structure

```text
universal-file-converter/
├── app.py              # Streamlit web interface (upload, format picker, ZIP download)
├── web_engines.py      # Conversion routing engine (LibreOffice, Calibre, PyMuPDF, Pillow)
├── requirements.txt    # Python dependencies
├── packages.txt        # System-level Linux packages (LibreOffice & Calibre) for cloud hosting
└── README.md           # Project documentation
```

---

## 🚀 Deploy Online for Free (Streamlit Community Cloud)

You can host this web app publicly for **\$0** using GitHub and Streamlit Community Cloud:

1. **Create a GitHub Repository:**
   * Create a new public repository on [GitHub](https://github.com) and upload `app.py`, `web_engines.py`, `requirements.txt`, `packages.txt`, and `README.md`.
2. **Connect to Streamlit Community Cloud:**
   * Sign in at [share.streamlit.io](https://streamlit.io) using your GitHub account.
   * Click **Create app** → **Yep, I have an app**.
   * Select your repository, set **Main file path** to `app.py`, and click **Deploy**.
3. **Share Your Link:**
   * Streamlit automatically installs Python libraries (`requirements.txt`) alongside LibreOffice and Calibre (`packages.txt`) and generates a shareable public URL.[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://documentconversion.streamlit.app/)

---

## 💻 Run Locally on Your Computer

### Prerequisites
* **Python 3.10+** installed and added to PATH.
* **LibreOffice** installed (for Office document conversions).
* **Calibre** installed *(optional, required for `.epub`, `.mobi`, `.azw3`, and `.djvu` conversions)*.

### Steps
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the web app:**
   ```bash
   streamlit run app.py
   ```
3. **Open in browser:**
   * Your browser will automatically open `http://localhost:8501`.

---

## ⚙️ How It Works
* **Office & PDF Conversions:** Routed through headless **LibreOffice** (`soffice`) and **pdf2docx** to preserve page layouts, tables, and formatting.
* **High-Resolution Images & XPS:** Rendered at 300 DPI using **PyMuPDF** and **Pillow**.
* **E-Books & DjVu:** Handled natively via **Calibre's** `ebook-convert` CLI.
* **Temporary Sandboxing:** Every user session runs inside an isolated temporary directory that is automatically wiped after the ZIP download is generated.
