__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import os
import cssclean.main
from cssclean.logger import logger


def main(args, extra):

    cleaner = cssclean.main.Cleaner()
    res = cleaner.clean(
        css=args.css,
        html=args.html,
        outdir=args.outdir,
        in_place=args.in_place,
        minify=args.minify,
        dry_run=args.dry_run,
    )

    # Dry run does not produce any results
    if args.dry_run:
        return
    logger.info(f"{len(res)} files written:")
    for original, filename in res.items():
        basename = os.path.basename(original)
        logger.info(f"  {basename} => {filename}")
