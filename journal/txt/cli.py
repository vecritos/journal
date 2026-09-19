from argparse import Namespace


def remove_duplicates(args: Namespace) -> int:
    from journal.txt.remove_duplicates import remove_duplicates as remove_duplicate_lines

    remove_duplicate_lines(args.input, args.output)
    return 0


def remove_whitespace(args: Namespace) -> int:
    from journal.txt.remove_whitespace import strip_newlines

    strip_newlines(args.input, args.output)
    return 0


def replace_characters(args: Namespace) -> int:
    from journal.txt.replace_characters import replace_chars

    replace_chars(args.input, args.old.replace("newline", "\n"), args.new.replace("newline", "\n"))
    return 0


def expand_timestamp(args: Namespace) -> int:
    from journal.txt.expand_timestamp import get_file_explanation

    get_file_explanation(args.input)
    return 0


def stamps_bulk_read(args: Namespace) -> int:
    from journal.txt.stamps_bulk_read import stamps_bulk_read as read_stamps

    read_stamps(args.add_newline)
    return 0
