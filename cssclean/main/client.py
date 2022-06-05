__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import os
import re
import tinycss2
import cssclean.utils as utils
from cssclean.logger import logger
import bs4


def collect_files(contenders, ext):
    """
    Collect files based on allowed extension.
    """
    paths = []
    for path in contenders or []:
        if path == ".":
            path = os.getcwd()
        if (
            os.path.isfile(path)
            and path.endswith(ext)
            and ".clean" not in os.path.basename(path)
        ):
            paths.append(path)
        elif os.path.isdir(path):
            for p in utils.recursive_find(path):
                if (
                    os.path.isfile(p)
                    and p.endswith(ext)
                    and "clean" not in os.path.basename(p)
                ):
                    paths.append(p)
    return paths


class Cleaner:
    def clean(
        self, css, html, outdir=None, in_place=False, dry_run=False, minify=False
    ):
        """
        Perform a clean operation.
        """
        css = collect_files(css, ".css")
        html = collect_files(html, ".html")
        if not css or not html:
            logger.exit("No html and/or css files detected - check paths!")

        # Read in html and derive classes and div types
        elements = self.collect_html_elements(html)

        # Also read in style components
        styles = self.collect_styles(css)

        # Filter to a final set
        styles = self.filter_rules(elements, styles)

        # Are we doing a dry run? Just print
        if dry_run:
            return self.do_print(styles, minify)

        # Out directory takes preference to in place
        return self.save_styles(styles, outdir, in_place=in_place, minify=minify)

    def save_styles(self, styles, outdir=None, in_place=False, minify=False):
        """
        Save styles to file.
        """
        files = {}
        for filename, sheet in styles.items():
            rest, ext = os.path.splitext(filename)
            outfile = rest + ".clean"
            if minify:
                outfile += ".min"
            outfile += ext
            basename = os.path.basename(outfile)
            if outdir is not None:
                outfile = os.path.join(outdir, basename)
            elif in_place:
                outfile = filename
            if minify:
                utils.write_file(self.minify(sheet), outfile)
            else:
                utils.write_file(self.write_sheet(sheet), outfile)
            files[filename] = outfile
        return files

    def write_sheet(self, sheet):
        """
        Write a sheet to file, not minimized
        """
        return "".join([x.serialize() for x in sheet])

    def do_print(self, styles, minify=False):
        """
        Print styles to the screen
        """
        for filename, sheet in styles.items():
            logger.info(filename)
            if minify:
                print(self.minify(sheet))
                continue
            for rule in sheet:
                print(rule.serialize())

    def minify(self, sheet):
        """
        Given a list of rules, minify (remove comments, whitespace, newlines)
        """
        sheet = [x for x in sheet if not isinstance(x, tinycss2.ast.Comment)]
        return "".join([re.sub("[\r\n ]+", "", x.serialize()) for x in sheet])

    def filter_rules(self, elements, styles):
        """
        Given a set of elements (classes and divs) and style sheets, filter
        each style sheet down to classes / ids used.
        """
        # selectors that are used - we aren't distinguishing between classes/divs
        # this is a lazy and more conservative approach that at worst will
        # have styling for an extra class / div with the same name
        selectors = elements["classes"].union(elements["divs"]).union(elements["ids"])

        for filename, sheet in styles.items():

            basename = os.path.basename(filename)
            logger.info(f"Sheet {basename} has {len(sheet)} rules.")

            # Updated set of rules
            rules = []
            for rule in sheet:
                # We are conservative and don't try to break apart rules
                if self.include_rule(rule, selectors):
                    rules.append(rule)

            styles[filename] = rules
            logger.info(f"Sheet {basename} filtered down to {len(rules)} rules.")

        return styles

    def include_rule(self, rule, selectors):
        """
        Determine if a rule should be included based on known selectors.

        To be conservative we don't break apart rules. We could do this
        if we are willing to also parse the extra tokens.
        """
        keepers = ["root"]
        if isinstance(rule, tinycss2.ast.Comment):
            return True
        if isinstance(rule, tinycss2.ast.WhitespaceToken):
            return False

        # Keep these, would require deeper parsing (open issue if interested)
        if rule.type == "at-rule" and rule.at_keyword in ["keyframes", "import"]:
            return True

        # Check components list based on type
        # E.g., max width - we have to check components inside
        if rule.type == "at-rule":
            comps = rule.content or []
        else:
            comps = rule.prelude or []
        for r in comps:
            if self._is_qualifier(r):
                continue
            if getattr(r, "is_identifier", False) == True and r.value in selectors:
                return True
            if r.type == "ident" and r.value in keepers or r.value in selectors:
                return True

    def _is_qualifier(self, r):
        """
        A qualifier component is not relevant to making an inclusion decision
        """
        if isinstance(r, tinycss2.ast.SquareBracketsBlock):
            return True
        if isinstance(r, tinycss2.ast.CurlyBracketsBlock):
            return True
        if isinstance(r, tinycss2.ast.FunctionBlock):
            return True
        return False

    def collect_styles(self, files):
        """
        Assemble list of styles
        """
        sheets = {}
        for filename in files:
            sheets[filename] = tinycss2.parse_stylesheet(utils.read_file(filename))
        return sheets

    def collect_html_elements(self, files):
        """
        Collect html elements and classes using beautiful soup
        """
        elements = {"classes": set(), "divs": set(), "ids": set()}
        for filename in files:
            soup = bs4.BeautifulSoup(utils.read_file(filename), "html.parser")

            for e in soup.find_all():
                elements["divs"].add(e.name)

                # Add specific classes
                if "class" in e.attrs:
                    [elements["classes"].add(x) for x in e["class"]]
                if "id" in e.attrs:
                    elements["ids"].add(e["id"])
        return elements
