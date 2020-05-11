import sys


import inspect

from mkdocs.__main__ import cli
from mkdocstrings.handlers import python as python_handler


def rebuild_category_lists(obj: dict) -> None:
    """
    Recursively rebuild the category lists of a collected object.
    Since `pytkdocs` dumps JSON on standard output, it must serialize the object-tree and flatten it to reduce data
    duplication and avoid cycle-references. Indeed, each node of the object-tree has a `children` list, containing
    all children, and another list for each category of children: `attributes`, `classes`, `functions`, `methods`
    and `modules`. It replaces the values in category lists with only the paths of the objects.
    Here, we reconstruct these category lists by picking objects in the `children` list using their path.
    For each object, we recurse on every one of its children.
    Args:
        obj: The collected object, loaded back from JSON into a Python dictionary.
    """
    obj["attributes"] = [obj["children"][path] for path in obj["attributes"]]
    obj["classes"] = [obj["children"][path] for path in obj["classes"]]
    obj["functions"] = [obj["children"][path] for path in obj["functions"]]
    obj["methods"] = [obj["children"][path] for path in obj["methods"]]
    obj["modules"] = [obj["children"][path] for path in obj["modules"]]
    obj["children"] = [v for k, v in obj["children"].items()]
    for child in obj["children"]:
        rebuild_category_lists(child)

    # Workaround for https://github.com/pawamoy/mkdocstrings/issues/108
    for section in obj['docstring_sections']:
        if section['type'] == 'markdown':
            section['value'] = section['value'].\
                replace('<', '&lt;').\
                replace('>', '&gt;')
        elif section['type'] == 'parameters':
            for item in section['value']:
                item['description'] = item['description'].\
                    replace('<', '&lt;').\
                    replace('>', '&gt;')
        elif section['type'] == 'return':
            section['value']['description'] = section['value']['description'].\
                replace('<', '&lt;').\
                replace('>', '&gt;')


python_handler.rebuild_category_lists = rebuild_category_lists


if __name__ == '__main__':
    sys.exit(cli())
