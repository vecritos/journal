from argparse import Namespace


def list_metadata(args: Namespace) -> int:
    from journal.metadata.img_metadata import list_metadata as list_image_metadata

    list_image_metadata(args.input, args.verbose)
    return 0


def wipe(args: Namespace) -> int:
    from journal.metadata.img_metadata import wipe_metadata

    wipe_metadata(args.input, args.output)
    return 0


def remove(args: Namespace) -> int:
    from journal.metadata.img_metadata import remove_keys

    remove_keys(args.input, args.keys, args.output)
    return 0


def add(args: Namespace) -> int:
    from journal.metadata.img_metadata import add_metadata

    add_metadata(args.input, args.keys, args.output)
    return 0
