import os
from PyPDF2 import PdfReader, PdfWriter

def compress_pdf(input_path):
    output_path = os.path.splitext(input_path)[0] + "_compressed.pdf"
    
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
