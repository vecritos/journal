# Journal

A Python-based command-line toolkit for journaling, document processing, note consolidation, and general file utilities.

Journal provides a single CLI for working with common files used in personal notes, archives, and document workflows. The project brings PDF manipulation, text processing, image metadata management, QR-code generation, and related utilities under one extensible command-line interface.

## Features

### PDF Utilities

Work with PDF documents directly from the command line.

- Merge multiple PDF files
- Rotate PDFs
- Extract selected pages
- Convert Markdown to PDF
- Convert plain text to PDF
- Combine images into a PDF

Examples:

```bash
journal pdf merge --input a.pdf b.pdf --output merged.pdf

journal pdf rotate --input input.pdf --output rotated.pdf

journal pdf extract --input input.pdf --output pages.pdf --pages 1 3 5

journal pdf md-to-pdf --input note.md --output note.pdf

journal pdf txt-to-pdf --input note.txt --output note.pdf

journal pdf images-to-pdf --input img1.jpg img2.jpg --output out.pdf
```

### Text Utilities

Tools for cleaning and processing text-based notes and documents.

Current operations include:

- Removing duplicate lines
- Removing unnecessary whitespace
- Replacing characters
- Expanding timestamps
- Bulk timestamp processing

Examples:

```bash
journal txt remove-duplicates \
    --input notes.txt \
    --output deduped.txt

journal txt remove-whitespace \
    --input script.py \
    --output cleaned.py

journal txt replace-characters \
    --input text.txt \
    --old newline \
    --new " "

journal txt expand-timestamp \
    --input timestamps.txt

journal txt stamps-bulk-read --add-newline
```

### Image Metadata

Inspect and modify metadata associated with image files.

Supported operations include:

- Listing metadata
- Removing all metadata
- Removing selected metadata fields
- Adding metadata fields
- Optional verbose inspection

Examples:

```bash
journal img list --input image.png --verbose

journal img wipe \
    --input image.png \
    --output clean.png

journal img remove \
    --input image.png \
    --keys Author Software \
    --output clean.png

journal img add \
    --input image.png \
    --keys Author=Jane CaseID=42 \
    --output with_meta.png
```

### QR Codes

Generate QR codes from URLs or file paths.

```bash
journal qr url \
    --input https://example.com \
    --output qrcode.png

journal qr file \
    --input document.txt \
    --output qrcode.png
```

## Requirements

- Python 3.10 or newer
- pip

The project is packaged using `setuptools`.

## Installation

Clone the repository:

```bash
git clone https://github.com/vecritos/journal.git
cd journal
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Or on Windows:

```powershell
.venv\Scripts\activate
```

Install the project:

```bash
pip install .
```

For development, install it in editable mode:

```bash
pip install -e .
```

After installation, the `journal` command should be available from your terminal.

## Usage

Display the command-line help:

```bash
journal --help
```

Display the project's usage examples:

```bash
journal help
```

Commands are organized by category:

```text
journal
├── pdf
│   ├── merge
│   ├── rotate
│   ├── extract
│   ├── md-to-pdf
│   ├── txt-to-pdf
│   └── images-to-pdf
│
├── qr
│   ├── url
│   └── file
│
├── img
│   ├── list
│   ├── wipe
│   ├── remove
│   └── add
│
└── txt
    ├── remove-duplicates
    ├── remove-whitespace
    ├── replace-characters
    ├── expand-timestamp
    └── stamps-bulk-read
```

Individual commands provide their own help:

```bash
journal pdf merge --help
journal img wipe --help
journal txt remove-duplicates --help
```

## Project Goals

Journal is intended to provide a collection of small, composable command-line tools for managing personal documents and information.

Rather than requiring separate scripts for recurring document-processing tasks, the project organizes those operations behind a consistent CLI.

The project is designed around several principles:

- **Local-first processing** — files can be processed directly on the user's machine.
- **Simple CLI workflows** — common operations should require short, predictable commands.
- **Composable utilities** — individual operations should remain useful independently.
- **Extensibility** — additional document and journaling tools can be incorporated as the project grows.
- **Automation friendly** — commands should be usable interactively or from shell scripts and larger workflows.

## Development

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/vecritos/journal.git
cd journal

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Changes to the Python source will then be reflected without reinstalling the package.

You can test the CLI with:

```bash
journal --help
```

or:

```bash
python -m journal
```

## Status

Journal is currently under active development.

The command structure, APIs, and available utilities may change as the project evolves.

The current package version is:

```text
0.1.0
```

## AI Assistance

This project was developed with occasional assistance from AI tools used as technical references and brainstorming aids.

AI assistance has been used for activities such as:

- Discussing software architecture
- Exploring implementation strategies
- Researching technical approaches
- Generating reference examples and library snippets

Final architecture, implementation decisions, integration, testing, debugging, and maintenance remain the responsibility of the project author.

AI tools consulted during development have included models and services from OpenAI, Google, and Microsoft.

## Contributing

The project is still evolving, but issues, suggestions, and contributions are welcome.

When contributing:

1. Fork the repository.
2. Create a branch for your change.
3. Keep changes focused and documented.
4. Test the affected CLI commands.
5. Submit a pull request describing the change and its purpose.

## License

Journal is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See `LICENSE` for the full license text.

---

Built as a growing collection of practical tools for working with journals, notes, documents, and personal data from the command line.
