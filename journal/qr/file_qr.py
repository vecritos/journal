from __future__ import annotations

from pathlib import Path


def file_to_qrcode(file_path: str | Path, output_file: str | Path = "file_qrcode.png") -> Path:
    try:
        import qrcode
    except ImportError as error:
        raise RuntimeError("QR export requires the qrcode package") from error

    source = Path(file_path)
    if not source.exists():
        raise FileNotFoundError(source)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(source.resolve().as_posix())
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(output_path)
    print(f"QR code saved to: {output_path.resolve()}")
    return output_path


__all__ = ["file_to_qrcode"]
