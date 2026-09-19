from argparse import Namespace


def url(args: Namespace) -> int:
    from journal.qr.url_qr import url_to_qrcode

    url_to_qrcode(args.input, args.output)
    return 0


def file(args: Namespace) -> int:
    from journal.qr.file_qr import file_to_qrcode

    file_to_qrcode(args.input, args.output)
    return 0
