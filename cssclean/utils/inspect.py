__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import inspect
import importlib
import sys
import os


def dynamic_import(name, path, allow_repeats=False):
    """
    Given a module name and filepath, iterate and return the modules to import

    Usage:

    here = os.path.abspath(os.path.dirname(__file__))
    for obj, imported in utils.dynamic_import(__name__, here):
        globals()[obj] = imported
    """
    module_files = list_modules(path)
    seen = set()
    for module_file in module_files:
        module_name = (
            name + "." + module_file.replace(path + os.path.sep, "").replace(".py", "")
        )
        imported_module = import_module(module_name, module_file)

        # Add everything to this
        for obj in dir(imported_module):

            # We only care about classes (steps)
            new_module = imported_module.__dict__[obj]
            if not inspect.isclass(new_module):
                continue

            # Skip private functions, etc.
            if obj.startswith("_"):
                continue
            if obj in seen and not allow_repeats:
                sys.exit("Repeated import %s found nested in %s" % (obj, module_name))
            yield obj, new_module
            seen.add(obj)


def list_modules(path):
    """
    Given a path, list public python modules
    """
    module_files = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                module_files.append(os.path.join(path, root, filename))
    return module_files


def import_module(module_name, module_file):
    """
    Import a module (based on filename) into module name.
    """
    module_spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
