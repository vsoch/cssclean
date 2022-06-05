#!/usr/bin/env python

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


import cssclean
from cssclean.logger import setup_logger
import argparse
import sys


def get_parser():
    parser = argparse.ArgumentParser(description="CSS Cleaner")
    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="show version and exit.",
        default=False,
        action="store_true",
    )

    # Logging
    logging_group = parser.add_argument_group("LOGGING")

    logging_group.add_argument(
        "--quiet",
        dest="quiet",
        help="suppress logging.",
        default=False,
        action="store_true",
    )

    logging_group.add_argument(
        "--verbose",
        dest="verbose",
        help="verbose output for logging.",
        default=False,
        action="store_true",
    )

    logging_group.add_argument(
        "--log-disable-color",
        dest="disable_color",
        default=False,
        help="Disable color for snakeface logging.",
        action="store_true",
    )

    logging_group.add_argument(
        "--log-use-threads",
        dest="use_threads",
        action="store_true",
        help="Force threads rather than processes.",
    )

    subparsers = parser.add_subparsers(
        help="actions", title="actions", description="actions", dest="command"
    )

    clean = subparsers.add_parser(
        "clean", help="clean a set of css files based on usage in html"
    )
    clean.add_argument(
        "--css", "-c", action="append", help="A css file or folder to include",
    )
    clean.add_argument(
        "--html", "-t", action="append", help="An html file or directory to include",
    )
    clean.add_argument(
        "--dry-run",
        dest="dry_run",
        help="Preview changes only",
        default=False,
        action="store_true",
    )
    clean.add_argument(
        "--minify",
        dest="minify",
        help="Minify new files",
        default=False,
        action="store_true",
    )
    clean.add_argument(
        "--in-place",
        "-i",
        dest="in_place",
        help="Write new files in place",
        default=False,
        action="store_true",
    )
    clean.add_argument(
        "--outdir", "-o", help="Write cleaned css files to output directory",
    )
    return parser


def main():

    parser = get_parser()

    def help(return_code=0):
        print("cssclean v.%s" % cssclean.__version__)
        parser.print_help()
        sys.exit(return_code)

    args, extra = parser.parse_known_args()

    setup_logger(
        quiet=args.quiet,
        nocolor=args.disable_color,
        debug=args.verbose,
        use_threads=args.use_threads,
    )

    # Show the version and exit
    if args.version is True:
        print(ohno.__version__)
        sys.exit(0)

    if args.command == "clean":
        from .clean import main
    else:
        help()

    # Pass on to the correct parser
    return_code = 0
    #    try:
    main(args, extra)
    sys.exit(return_code)
    #   except UnboundLocalError:
    #      return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
