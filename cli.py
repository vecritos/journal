import argparse

from journal.metadata import cli as metadata_cli
from journal.pdf import cli as pdf_cli
from journal.qr import cli as qr_cli
from journal.txt import cli as txt_cli


def _add_common_input_output(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument("--input", required=True, help="Input file path")
    subparser.add_argument("--output", required=True, help="Output file path")


HELP_TEXT = """Usage examples:

journal pdf merge --input a.pdf b.pdf --output merged.pdf
journal pdf rotate --input input.pdf --output rotated.pdf
journal pdf extract --input input.pdf --output pages.pdf --pages 1 3 5
journal pdf md-to-pdf --input note.md --output note.pdf
journal pdf txt-to-pdf --input note.txt --output note.pdf
journal pdf images-to-pdf --input img1.jpg img2.jpg --output out.pdf

journal qr url --input https://example.com --output qrcode.png
journal qr file --input document.txt --output qrcode.png

journal img list --input image.png --verbose
journal img wipe --input image.png --output clean.png
journal img remove --input image.png --keys Author Software --output clean.png
journal img add --input image.png --keys Author=Jane CaseID=42 --output with_meta.png

journal txt remove-duplicates --input notes.txt --output deduped.txt
journal txt remove-whitespace --input script.py --output cleaned.py
journal txt replace-characters --input text.txt --old newline --new " "
journal txt expand-timestamp --input timestamps.txt
journal txt stamps-bulk-read --add-newline
"""


def _show_help(_args: argparse.Namespace) -> int:
    print(HELP_TEXT, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="journal", description="Journal command line utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    help_parser = subparsers.add_parser("help", help="Show usage examples for the journal CLI")
    help_parser.set_defaults(handler=_show_help)

    pdf_parser = subparsers.add_parser("pdf", help="PDF-related operations")
    pdf_subparsers = pdf_parser.add_subparsers(dest="pdf_command", required=True)

    merge = pdf_subparsers.add_parser("merge", help="Merge multiple PDFs")
    merge.set_defaults(handler=pdf_cli.merge)
    merge.add_argument("--input", nargs="+", required=True, help="Input PDFs to merge")
    merge.add_argument("--output", required=True, help="Output merged PDF path")

    rotate = pdf_subparsers.add_parser("rotate", help="Rotate a PDF by 90 degrees")
    rotate.set_defaults(handler=pdf_cli.rotate)
    _add_common_input_output(rotate)

    extract = pdf_subparsers.add_parser("extract", help="Extract selected pages from a PDF")
    extract.set_defaults(handler=pdf_cli.extract)
    extract.add_argument("--input", required=True, help="Input PDF path")
    extract.add_argument("--output", required=True, help="Output PDF path")
    extract.add_argument("--pages", nargs="+", required=True, help="Pages to extract, e.g. 1 3 5")

    md_to_pdf = pdf_subparsers.add_parser("md-to-pdf", help="Convert Markdown to PDF")
    md_to_pdf.set_defaults(handler=pdf_cli.markdown_to_pdf)
    _add_common_input_output(md_to_pdf)

    txt_to_pdf = pdf_subparsers.add_parser("txt-to-pdf", help="Convert text to PDF")
    txt_to_pdf.set_defaults(handler=pdf_cli.text_to_pdf)
    _add_common_input_output(txt_to_pdf)

    images_to_pdf = pdf_subparsers.add_parser("images-to-pdf", help="Create PDF from images")
    images_to_pdf.set_defaults(handler=pdf_cli.images_to_pdf)
    images_to_pdf.add_argument("--input", nargs="+", required=True, help="Image files to include")
    images_to_pdf.add_argument("--output", required=True, help="Output PDF path")

    qr_parser = subparsers.add_parser("qr", help="Create QR codes")
    qr_subparsers = qr_parser.add_subparsers(dest="qr_command", required=True)

    qr_url = qr_subparsers.add_parser("url", help="Create a QR from a URL")
    qr_url.set_defaults(handler=qr_cli.url)
    qr_url.add_argument("--input", required=True, help="URL to encode")
    qr_url.add_argument("--output", default="qrcode.png", help="Output image path")

    qr_file = qr_subparsers.add_parser("file", help="Create a QR from a file path")
    qr_file.set_defaults(handler=qr_cli.file)
    qr_file.add_argument("--input", required=True, help="File path to encode")
    qr_file.add_argument("--output", default="file_qrcode.png", help="Output image path")

    img_parser = subparsers.add_parser("img", help="Image metadata operations")
    img_subparsers = img_parser.add_subparsers(dest="img_command", required=True)

    img_list = img_subparsers.add_parser("list", help="List image metadata")
    img_list.set_defaults(handler=metadata_cli.list_metadata)
    img_list.add_argument("--input", required=True, help="Image file to inspect")
    img_list.add_argument("--verbose", action="store_true", help="Include pixel hash output")

    img_wipe = img_subparsers.add_parser("wipe", help="Remove all metadata from an image")
    img_wipe.set_defaults(handler=metadata_cli.wipe)
    img_wipe.add_argument("--input", required=True, help="Image file to sanitize")
    img_wipe.add_argument("--output", help="Optional output path")

    img_remove = img_subparsers.add_parser("remove", help="Remove specific metadata keys")
    img_remove.set_defaults(handler=metadata_cli.remove)
    img_remove.add_argument("--input", required=True, help="Image file")
    img_remove.add_argument("--keys", nargs="+", required=True, help="Metadata keys to remove")
    img_remove.add_argument("--output", help="Optional output path")

    img_add = img_subparsers.add_parser("add", help="Add metadata to an image")
    img_add.set_defaults(handler=metadata_cli.add)
    img_add.add_argument("--input", required=True, help="Image file")
    img_add.add_argument("--keys", nargs="+", required=True, help="Entries like Author=Jane")
    img_add.add_argument("--output", help="Optional output path")

    txt_parser = subparsers.add_parser("txt", help="Text utilities")
    txt_subparsers = txt_parser.add_subparsers(dest="txt_command", required=True)

    txt_remove_duplicates = txt_subparsers.add_parser("remove-duplicates", help="Remove duplicate lines from a text file")
    txt_remove_duplicates.set_defaults(handler=txt_cli.remove_duplicates)
    txt_remove_duplicates.add_argument("--input", required=True, help="Input text file")
    txt_remove_duplicates.add_argument("--output", default="export.txt", help="Output text file")

    txt_remove_whitespace = txt_subparsers.add_parser("remove-whitespace", help="Strip unnecessary whitespace from a text file")
    txt_remove_whitespace.set_defaults(handler=txt_cli.remove_whitespace)
    txt_remove_whitespace.add_argument("--input", required=True, help="Input text file")
    txt_remove_whitespace.add_argument("--output", default="output.py", help="Output text file")

    txt_replace_chars = txt_subparsers.add_parser("replace-characters", help="Replace character sequences within a text file")
    txt_replace_chars.set_defaults(handler=txt_cli.replace_characters)
    txt_replace_chars.add_argument("--input", required=True, help="Input text file")
    txt_replace_chars.add_argument("--old", required=True, help="Original text to replace; use 'newline' for newline")
    txt_replace_chars.add_argument("--new", required=True, help="Replacement text; use 'newline' for newline")

    txt_expand_timestamp = txt_subparsers.add_parser("expand-timestamp", help="Interactively expand timestamp entries from a file")
    txt_expand_timestamp.set_defaults(handler=txt_cli.expand_timestamp)
    txt_expand_timestamp.add_argument("--input", required=True, help="Input file with timestamp lines")

    txt_bulk_read = txt_subparsers.add_parser("stamps-bulk-read", help="Read tracked stamps files in bulk")
    txt_bulk_read.set_defaults(handler=txt_cli.stamps_bulk_read)
    txt_bulk_read.add_argument("--add-newline", action="store_true", help="Add a newline after each file")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
