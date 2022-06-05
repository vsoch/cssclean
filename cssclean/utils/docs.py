__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import sys


def get_docstring(step_module):
    if not step_module.__doc__:
        sys.exit("module %s is missing a docstring" % (step_module))
    docs = [x.strip() for x in step_module.__doc__.split("\n") if x and x.strip()]
    if not docs:
        sys.exit("module %s is missing a docstring" % (step_module))
    return docs
