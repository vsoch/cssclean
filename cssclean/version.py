__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.0.11"
AUTHOR = "Vanessa Sochat"
EMAIL = "vsoch@users.noreply.github.com"
NAME = "cssclean"
PACKAGE_URL = "https://github.com/vsoch/cssclean"
KEYWORDS = "css, cleaner"
DESCRIPTION = "remove un-used css from a file"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("tinycss2", {"min_version": None}),
    ("beautifulsoup4", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

################################################################################
# Submodule Requirements

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
