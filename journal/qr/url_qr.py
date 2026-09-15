from __future__ import annotations

from pathlib import Path


def url_to_qrcode(url: str, output_file: str | Path = "qrcode.png") -> Path:
    try:
        import qrcode
    except ImportError as error:
        raise RuntimeError("QR export requires the qrcode package") from error

    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    qr.make_image(fill_color="black", back_color="white").save(output_path)
    print(f"QR code saved to: {output_path.resolve()}")
    return output_path


__all__ = ["url_to_qrcode"]

