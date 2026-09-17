import argparse
from pathlib import Path


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="journal", description="Journal command line utilities")
    subparsers = parser.add_subparsers(dest="command")

    help_parser = subparsers.add_parser("help", help="Show usage examples for the journal CLI")
    help_parser.set_defaults(command="help")

    pdf_parser = subparsers.add_parser("pdf", help="PDF-related operations")
    pdf_subparsers = pdf_parser.add_subparsers(dest="pdf_command", required=True)

    merge = pdf_subparsers.add_parser("merge", help="Merge multiple PDFs")
    merge.add_argument("--input", nargs="+", required=True, help="Input PDFs to merge")
    merge.add_argument("--output", required=True, help="Output merged PDF path")

    rotate = pdf_subparsers.add_parser("rotate", help="Rotate a PDF by 90 degrees")
    _add_common_input_output(rotate)

    extract = pdf_subparsers.add_parser("extract", help="Extract selected pages from a PDF")
    extract.add_argument("--input", required=True, help="Input PDF path")
    extract.add_argument("--output", required=True, help="Output PDF path")
    extract.add_argument("--pages", nargs="+", required=True, help="Pages to extract, e.g. 1 3 5")

    md_to_pdf = pdf_subparsers.add_parser("md-to-pdf", help="Convert Markdown to PDF")
    _add_common_input_output(md_to_pdf)

    txt_to_pdf = pdf_subparsers.add_parser("txt-to-pdf", help="Convert text to PDF")
    _add_common_input_output(txt_to_pdf)

    images_to_pdf = pdf_subparsers.add_parser("images-to-pdf", help="Create PDF from images")
    images_to_pdf.add_argument("--input", nargs="+", required=True, help="Image files to include")
    images_to_pdf.add_argument("--output", required=True, help="Output PDF path")

    qr_parser = subparsers.add_parser("qr", help="Create QR codes")
    qr_subparsers = qr_parser.add_subparsers(dest="qr_command", required=True)

    qr_url = qr_subparsers.add_parser("url", help="Create a QR from a URL")
    qr_url.add_argument("--input", required=True, help="URL to encode")
    qr_url.add_argument("--output", default="qrcode.png", help="Output image path")

    qr_file = qr_subparsers.add_parser("file", help="Create a QR from a file path")
    qr_file.add_argument("--input", required=True, help="File path to encode")
    qr_file.add_argument("--output", default="file_qrcode.png", help="Output image path")

    img_parser = subparsers.add_parser("img", help="Image metadata operations")
    img_subparsers = img_parser.add_subparsers(dest="img_command", required=True)

    img_list = img_subparsers.add_parser("list", help="List image metadata")
    img_list.add_argument("--input", required=True, help="Image file to inspect")
    img_list.add_argument("--verbose", action="store_true", help="Include pixel hash output")

    img_wipe = img_subparsers.add_parser("wipe", help="Remove all metadata from an image")
    img_wipe.add_argument("--input", required=True, help="Image file to sanitize")
    img_wipe.add_argument("--output", help="Optional output path")

    img_remove = img_subparsers.add_parser("remove", help="Remove specific metadata keys")
    img_remove.add_argument("--input", required=True, help="Image file")
    img_remove.add_argument("--keys", nargs="+", required=True, help="Metadata keys to remove")
    img_remove.add_argument("--output", help="Optional output path")

    img_add = img_subparsers.add_parser("add", help="Add metadata to an image")
    img_add.add_argument("--input", required=True, help="Image file")
    img_add.add_argument("--keys", nargs="+", required=True, help="Entries like Author=Jane")
    img_add.add_argument("--output", help="Optional output path")

    txt_parser = subparsers.add_parser("txt", help="Text utilities")
    txt_subparsers = txt_parser.add_subparsers(dest="txt_command", required=True)

    txt_remove_duplicates = txt_subparsers.add_parser("remove-duplicates", help="Remove duplicate lines from a text file")
    txt_remove_duplicates.add_argument("--input", required=True, help="Input text file")
    txt_remove_duplicates.add_argument("--output", default="export.txt", help="Output text file")

    txt_remove_whitespace = txt_subparsers.add_parser("remove-whitespace", help="Strip unnecessary whitespace from a text file")
    txt_remove_whitespace.add_argument("--input", required=True, help="Input text file")
    txt_remove_whitespace.add_argument("--output", default="output.py", help="Output text file")

    txt_replace_chars = txt_subparsers.add_parser("replace-characters", help="Replace character sequences within a text file")
    txt_replace_chars.add_argument("--input", required=True, help="Input text file")
    txt_replace_chars.add_argument("--old", required=True, help="Original text to replace; use 'newline' for newline")
    txt_replace_chars.add_argument("--new", required=True, help="Replacement text; use 'newline' for newline")

    txt_expand_timestamp = txt_subparsers.add_parser("expand-timestamp", help="Interactively expand timestamp entries from a file")
    txt_expand_timestamp.add_argument("--input", required=True, help="Input file with timestamp lines")

    txt_bulk_read = txt_subparsers.add_parser("stamps-bulk-read", help="Read tracked stamps files in bulk")
    txt_bulk_read.add_argument("--add-newline", action="store_true", help="Add a newline after each file")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "help":
        print(HELP_TEXT, end="")
        return 0

    if args.command == "pdf":
        if args.pdf_command == "merge":
            from journal.pdf.merge_pdfs import merge_pdfs
            merge_pdfs(args.input, args.output)
        elif args.pdf_command == "rotate":
            from journal.pdf.rotate_pdf_90 import rotate_pdf_90
            rotate_pdf_90(Path(args.input), Path(args.output))
        elif args.pdf_command == "extract":
            from journal.pdf.extract_first_page import extract_first_page
            extract_first_page(Path(args.input), [int(p) for p in args.pages], Path(args.output))
        elif args.pdf_command == "md-to-pdf":
            from journal.pdf.md_to_pdf import md_to_pdf
            md_to_pdf(Path(args.input), Path(args.output))
        elif args.pdf_command == "txt-to-pdf":
            from journal.pdf.txt_to_pdf import txt_to_pdf
            txt_to_pdf(Path(args.input), Path(args.output))
        elif args.pdf_command == "images-to-pdf":
            from journal.pdf.images_to_pdf_sorted import images_to_pdf_sorted
            images_to_pdf_sorted(args.input, Path(args.output))
        else:
            parser.error(f"Unsupported PDF command: {args.pdf_command}")
        return 0

    if args.command == "qr":
        if args.qr_command == "url":
            from journal.qr.url_qr import url_to_qrcode
            url_to_qrcode(args.input, args.output)
            return 0
        if args.qr_command == "file":
            from journal.qr.file_qr import file_to_qrcode
            file_to_qrcode(args.input, args.output)
            return 0
        parser.error(f"Unsupported QR command: {args.qr_command}")
        return 2

    if args.command == "img":
        from journal.metadata.img_metadata import add_metadata, list_metadata, remove_keys, wipe_metadata

        if args.img_command == "list":
            list_metadata(args.input, args.verbose)
            return 0
        if args.img_command == "wipe":
            wipe_metadata(args.input, args.output)
            return 0
        if args.img_command == "remove":
            remove_keys(args.input, args.keys, args.output)
            return 0
        if args.img_command == "add":
            add_metadata(args.input, args.keys, args.output)
            return 0
        parser.error(f"Unsupported image metadata command: {args.img_command}")
        return 2

    if args.command == "txt":
        if args.txt_command == "remove-duplicates":
            from journal.txt.remove_duplicates import remove_duplicates
            remove_duplicates(args.input, args.output)
            return 0
        if args.txt_command == "remove-whitespace":
            from journal.txt.remove_whitespace import strip_newlines
            strip_newlines(args.input, args.output)
            return 0
        if args.txt_command == "replace-characters":
            from journal.txt.replace_characters import replace_chars
            replace_chars(args.input, args.old.replace("newline", "\n"), args.new.replace("newline", "\n"))
            return 0
        if args.txt_command == "expand-timestamp":
            from journal.txt.expand_timestamp import get_file_explanation
            get_file_explanation(args.input)
            return 0
        if args.txt_command == "stamps-bulk-read":
            from journal.txt.stamps_bulk_read import stamps_bulk_read
            stamps_bulk_read(args.add_newline)
            return 0
        parser.error(f"Unsupported text utility command: {args.txt_command}")
        return 2

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
