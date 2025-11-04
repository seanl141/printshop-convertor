from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path
from docx2pdf import convert
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pillow_heif import register_heif_opener
from PIL import Image
import shutil

register_heif_opener()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

converted_dir = Path("converted")
converted_dir.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert_docx")
async def convert_docx(file: UploadFile = File(...)):
    input_path = Path("temp_" + file.filename)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    convert(input_path)
    output_path = input_path.with_suffix(".pdf")
    dest = converted_dir / output_path.name
    shutil.move(output_path, dest)
    input_path.unlink(missing_ok=True)
    return FileResponse(dest, filename=dest.name)

@app.post("/convert_heic")
async def convert_heic(file: UploadFile = File(...)):
    input_path = Path("temp_" + file.filename)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    img = Image.open(input_path)
    output_path = converted_dir / (input_path.stem + ".jpg")
    img.save(output_path, "JPEG")
    input_path.unlink(missing_ok=True)
    return FileResponse(output_path, filename=output_path.name)

@app.post("/merge_pdfs")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    merger = PdfMerger()
    paths = []
    for f in files:
        p = Path("temp_" + f.filename)
        with open(p, "wb") as out:
            shutil.copyfileobj(f.file, out)
        merger.append(str(p))
        paths.append(p)
    output = converted_dir / "merged.pdf"
    merger.write(output)
    merger.close()
    for p in paths:
        p.unlink(missing_ok=True)
    return FileResponse(output, filename="merged.pdf")

@app.post("/split_pdf")
async def split_pdf(file: UploadFile = File(...)):
    input_path = Path("temp_" + file.filename)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    reader = PdfReader(input_path)
    split_files = []
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = converted_dir / f"{input_path.stem}_page{i+1}.pdf"
        with open(output_path, "wb") as out:
            writer.write(out)
        split_files.append(output_path)
    input_path.unlink(missing_ok=True)
    return FileResponse(split_files[0], filename=split_files[0].name)
