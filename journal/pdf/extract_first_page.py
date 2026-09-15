import sys
import pypdf

def extract_first_page(pdf_path, pages, output_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = pypdf.PdfReader(pdf_file)
        writer = pypdf.PdfWriter()

        for n in pages:
            page = reader.pages[int(n)]
            writer.add_page(page)

        # Write the first page to a new PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
