import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image
import pymupdf
from pdf2docx import Converter

WORD_EXTS = {".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".html", ".htm", ".xml"}
EXCEL_EXTS = {".xls", ".xlsx", ".ods", ".csv"}
PPT_EXTS = {".ppt", ".pptx", ".odp"}
IMG_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}
MUPDF_EXTS = {".pdf", ".xps", ".epub", ".mobi"}
CALIBRE_EXTS = {".epub", ".mobi", ".azw3", ".djvu"}

ALL_SUPPORTED_EXTS = [
    ext.lstrip(".") for ext in sorted(WORD_EXTS | EXCEL_EXTS | PPT_EXTS | IMG_EXTS | MUPDF_EXTS | CALIBRE_EXTS)
]

LIBREOFFICE_TARGETS = {"pdf", "docx", "doc", "odt", "rtf", "xlsx", "xls", "ods", "csv", "pptx", "ppt", "odp", "txt", "html"}
EBOOK_TARGETS = {"epub", "mobi", "azw3"}
IMAGE_TARGETS = {"jpg", "png", "tiff"}


def run_libreoffice(src_path, target_ext, out_dir):
    cmd = ["soffice", "--headless", "--convert-to", target_ext, "--outdir", out_dir, src_path]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    expected = os.path.join(out_dir, f"{Path(src_path).stem}.{target_ext}")
    if not os.path.exists(expected):
        raise RuntimeError(f"LibreOffice could not convert {Path(src_path).suffix} to .{target_ext}")
    return expected


def build_pdf_bridge(src_path, work_dir):
    ext = Path(src_path).suffix.lower()
    base_name = Path(src_path).stem
    pdf_bridge = os.path.join(work_dir, f"{base_name}_bridge.pdf")

    if ext == ".pdf":
        return src_path

    if ext in CALIBRE_EXTS:
        subprocess.run(["ebook-convert", src_path, pdf_bridge], check=True)
        return pdf_bridge

    if ext in MUPDF_EXTS:
        doc = pymupdf.open(src_path)
        with open(pdf_bridge, "wb") as f:
            f.write(doc.convert_to_pdf())
        doc.close()
        return pdf_bridge

    if ext in IMG_EXTS:
        Image.open(src_path).convert("RGB").save(pdf_bridge, "PDF", resolution=300.0)
        return pdf_bridge

    if ext in (WORD_EXTS | EXCEL_EXTS | PPT_EXTS):
        raw_pdf = run_libreoffice(src_path, "pdf", work_dir)
        os.replace(raw_pdf, pdf_bridge)
        return pdf_bridge

    raise RuntimeError(f"Unsupported source format: {ext}")


def convert_web_file(src_path, target_ext, out_dir):
    """Converts src_path into target_ext inside out_dir and returns a list of created file paths."""
    ext = Path(src_path).suffix.lower()
    base_name = Path(src_path).stem
    out_file = os.path.join(out_dir, f"{base_name}.{target_ext}")

    # 1. Image -> Image
    if ext in IMG_EXTS and target_ext in IMAGE_TARGETS:
        img = Image.open(src_path)
        if target_ext == "jpg" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        pil_fmt = "JPEG" if target_ext == "jpg" else target_ext.upper()
        img.save(out_file, pil_fmt)
        return [out_file]

    # 2. PDF -> Word (.docx) using pdf2docx for accurate layout reconstruction
    if ext == ".pdf" and target_ext == "docx":
        cv = Converter(src_path)
        cv.convert(out_file)
        cv.close()
        return [out_file]

    # 3. Direct Office -> Office / PDF via LibreOffice
    if ext in (WORD_EXTS | EXCEL_EXTS | PPT_EXTS) and target_ext in LIBREOFFICE_TARGETS:
        return [run_libreoffice(src_path, target_ext, out_dir)]

    # 4. E-Books (.epub, .mobi, .azw3, .djvu) via Calibre (except multi-page images)
    if (target_ext in EBOOK_TARGETS or ext in CALIBRE_EXTS) and target_ext not in IMAGE_TARGETS:
        subprocess.run(["ebook-convert", src_path, out_file], check=True)
        return [out_file]

    # 5. Universal PDF Bridge -> PDF, Multi-page Images, Text/Markup, or Word
    pdf_bridge = build_pdf_bridge(src_path, out_dir)

    if target_ext == "pdf":
        shutil.copy2(pdf_bridge, out_file)
        return [out_file]

    if target_ext in IMAGE_TARGETS:
        doc = pymupdf.open(pdf_bridge)
        created_images = []
        for idx, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=300)
            page_out = os.path.join(out_dir, f"{base_name}_page_{idx}.{target_ext}")
            if target_ext == "tiff":
                Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(page_out, "TIFF")
            else:
                pix.save(page_out)
            created_images.append(page_out)
        doc.close()
        return created_images

    if target_ext in {"txt", "md", "html", "xml"}:
        doc = pymupdf.open(pdf_bridge)
        mode = "text" if target_ext in {"txt", "md"} else target_ext
        sep = "\n\n---\n\n" if target_ext == "md" else "\n"
        content = sep.join(page.get_text(mode) for page in doc)
        doc.close()
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
        return [out_file]

    if target_ext == "docx":
        cv = Converter(pdf_bridge)
        cv.convert(out_file)
        cv.close()
        return [out_file]

    raise RuntimeError(f"Conversion from {ext} to .{target_ext} is not supported.")
