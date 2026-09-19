from argparse import Namespace
from pathlib import Path


def merge(args: Namespace) -> int:
    from journal.pdf.merge_pdfs import merge_pdfs

    merge_pdfs(args.input, args.output)
    return 0


def rotate(args: Namespace) -> int:
    from journal.pdf.rotate_pdf_90 import rotate_pdf_90

    rotate_pdf_90(Path(args.input), Path(args.output))
    return 0


def extract(args: Namespace) -> int:
    from journal.pdf.extract_first_page import extract_first_page

    extract_first_page(Path(args.input), [int(page) for page in args.pages], Path(args.output))
    return 0


def markdown_to_pdf(args: Namespace) -> int:
    from journal.pdf.md_to_pdf import md_to_pdf

    md_to_pdf(Path(args.input), Path(args.output))
    return 0


def text_to_pdf(args: Namespace) -> int:
    from journal.pdf.txt_to_pdf import txt_to_pdf

    txt_to_pdf(Path(args.input), Path(args.output))
    return 0


def images_to_pdf(args: Namespace) -> int:
    from journal.pdf.images_to_pdf_sorted import images_to_pdf_sorted

    images_to_pdf_sorted(args.input, Path(args.output))
    return 0
