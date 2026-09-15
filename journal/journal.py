#!/usr/bin/env python3
"""CLI-first journal with Markdown entries and optional media exports."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp", ".heic", ".heif"}


def entry_id(value: str | None = None) -> str:
    return (value or datetime.now().strftime("%Y-%m-%d-%H%M%S")).strip()


def entry_path(root: Path, identifier: str) -> Path:
    return root / "entries" / f"{identifier}.md"


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def create_entry(root: Path, identifier: str, title: str, body: str) -> Path:
    path = entry_path(root, identifier)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Entry already exists: {identifier}")

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    content = f"# {title.strip()}\n\nCreated: {timestamp}\n\n{body.rstrip()}\n"
    path.write_text(content, encoding="utf-8")
    return path


def list_entries(root: Path) -> list[Path]:
    return sorted((root / "entries").glob("*.md"), reverse=True)


def attach_image(root: Path, identifier: str, source: Path) -> Path:
    if source.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image format: {source.suffix}")
    if not source.is_file():
        raise FileNotFoundError(source)

    entry = entry_path(root, identifier)
    if not entry.is_file():
        raise FileNotFoundError(f"Entry does not exist: {identifier}")

    destination_dir = root / "attachments" / "images" / identifier
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    shutil.copy2(source, destination)

    relative_path = destination.relative_to(entry.parent).as_posix()
    with entry.open("a", encoding="utf-8") as file:
        file.write(f"\n\n![{source.stem}]({relative_path})\n")
    return destination


def export_pdf(root: Path, identifier: str, output: Path) -> None:
    try:
        from markdown_pdf import MarkdownPdf, Section
    except ImportError as error:
        raise RuntimeError("PDF export requires the markdown-pdf package") from error

    entry = entry_path(root, identifier)
    if not entry.is_file():
        raise FileNotFoundError(f"Entry does not exist: {identifier}")

    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(entry.read_text(encoding="utf-8")))
    pdf.save(output)


def create_qr(root: Path, identifier: str, value: str | None, output: Path) -> None:
    try:
        import qrcode
    except ImportError as error:
        raise RuntimeError("QR export requires the qrcode package") from error

    output.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q)
    qr.add_data(value or f"journal://{identifier}")
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a Markdown-based journal")
    parser.add_argument("--root", type=Path, default=Path("journal"), help="Journal data directory")
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", help="Create an entry")
    new.add_argument("title")
    new.add_argument("--id", dest="identifier")
    new.add_argument("--body", default="", help="Entry body; reads stdin when omitted")

    commands.add_parser("list", help="List entries")

    show = commands.add_parser("show", help="Print an entry")
    show.add_argument("identifier")

    attach = commands.add_parser("attach", help="Attach an image to an entry")
    attach.add_argument("identifier")
    attach.add_argument("image", type=Path)

    export = commands.add_parser("export", help="Export an entry as PDF")
    export.add_argument("identifier")
    export.add_argument("--output", type=Path)

    qr = commands.add_parser("qr", help="Create a QR code for an entry")
    qr.add_argument("identifier")
    qr.add_argument("--value", help="Value encoded in the QR code")
    qr.add_argument("--output", type=Path)
    return parser


def run(args: argparse.Namespace) -> int:
    root = args.root
    if args.command == "new":
        body = args.body if args.body else sys.stdin.read()
        path = create_entry(root, entry_id(args.identifier), args.title, body)
        print(path)
    elif args.command == "list":
        for path in list_entries(root):
            print(f"{path.stem}\t{read_title(path)}")
    elif args.command == "show":
        print(entry_path(root, args.identifier).read_text(encoding="utf-8"), end="")
    elif args.command == "attach":
        print(attach_image(root, args.identifier, args.image))
    elif args.command == "export":
        output = args.output or root / "exports" / f"{args.identifier}.pdf"
        export_pdf(root, args.identifier, output)
        print(output)
    elif args.command == "qr":
        output = args.output or root / "attachments" / "qrcodes" / f"{args.identifier}.png"
        create_qr(root, args.identifier, args.value, output)
        print(output)
    return 0


def main() -> int:
    parser = build_parser()
    try:
        return run(parser.parse_args())
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
