Seán Lawlor
Final-Year Computer Science Student, Trinity College Dublin
Built for internal use at a print shop to streamline daily file conversion tasks.

A lightweight, ad-free web app built in **Python (FastAPI)** for converting and managing files used in a print shop.  
It runs locally or can be deployed online for free (e.g. via [Render](https://render.com)).

---

## 🚀 Features

✅ **DOCX → PDF** conversion  
✅ **HEIC → JPG** conversion  
✅ **Merge multiple PDF files**  
✅ **Split a PDF into pages**  
✅ 100% local — **no uploads to external servers**  
✅ Easy to use via a web browser interface  

---

## 🧩 Tech Stack

- **Backend:** FastAPI (Python 3.12)  
- **Frontend:** HTML + CSS (Jinja2 templates)  
- **Libraries:**  
  - [`docx2pdf`](https://pypi.org/project/docx2pdf/)  
  - [`pillow-heif`](https://pypi.org/project/pillow-heif/) + [`Pillow`](https://pypi.org/project/Pillow/)  
  - [`PyPDF2`](https://pypi.org/project/PyPDF2/)  
  - [`Jinja2`](https://pypi.org/project/Jinja2/)  

---

## ⚙️ Installation

Clone the repo:
```bash
git clone https://github.com/seanl141/printshop-converter.git
cd printshop-converter
