#!/usr/bin/env python

"""Embiggen --- Simpler HTML.

Embiggen is a simple filter program that takes a CSS-like syntax, and
'embiggens' it, generating the corresponding HTML code.

Embiggen is under the 2-clause BSD license. See the COPYING file for details.

TODO: Multipliers.
TODO: Placeholders.
TODO: Command line options.
TODO: Shortcuts.
TODO: Default properties.
"""

import re
import sys
from xml.dom.minidom import Element, Text

def build(element_unparsed):
    """Builds an Element out of its string definition.

    An element is composed of:

    - A Name,
    - Optionally, a class, preceded by #,
    - Zero or more Classes, preceded and separated by `.`,
    - Zero or more Properties, wrapped in `[]`, and optionally separated
      by commas, and
    - Optionally, content, wrapped in {}.

    Some elements have inherent Properties (like `src` and `alt` for `img`).
    Others are inherently block elements (like `div`).
    """

    short_tags = ['area', 'base', 'basefont', 'br', 'embed', 'hr', 'input',
                  'img', 'link', 'param', 'meta']

    result = re.match(r'(\w+)'                        # Name
                      r'\s*(?:#(\w+))?'               # ID
                      r'((?:\.\w+)*)'                 # Classes
                      r'((?:\s*\[[^\]]+\])*)'         # Properties
                      r'(?:\s*\{(\s*[^\}]+)\s*\})?',  # Content
                      element_unparsed)

    name, id_, classes, properties, content = result.group(1, 2, 3, 4, 5)

    element = Element(name)

    if id_ is not None:
        element.setAttribute("id", id_)

    if classes is not None and classes != '':
        element.setAttribute("class", classes.replace('.', ' ').strip())

    if properties is not None:
        props = re.split(r'[\[\],]\s*', properties)
        for prop in props:
            if prop.strip() == '':
                continue

            if '=' in prop:
                prop_name, prop_value = prop.split('=')
            else:
                prop_name, prop_value = prop, ''

            element.setAttribute(prop_name.strip(), prop_value.strip())

    if content is None and name not in short_tags:
        content = ''

    if content is not None:
        text = Text()
        text.data = content.strip()
        element.appendChild(text)

    return element

def parse_element(line):
    """Parses a single element out of a line.

    Returns a triple of (element, separator, rest).
    """

    # This could be simplified. We only need to check that the separator isn't
    # inside `[]` or `{}`.
    result = re.search(r'(\w+(?:#\w+)?(?:\.\w+)*(?:\s*\[[^\]]+\])*(?:\s*\{[^\}]+\})?)'
                        '(?:\s*(<|\+|>)(.*))?', line)
    if result is not None:
        element_unparsed, separator, rest = result.group(1, 2, 3)

        return build(element_unparsed), separator, rest

def parse(line):
    """Parses a line, returning a tree representation of the result.

    The root node is a dummy anonymous element.
    """

    root = Element('')
    current_element = root
    rest = line

    while True:
        element, separator, rest = parse_element(rest)

        current_element.appendChild(element)

        if rest is None:
            break

        if separator == '<':
            current_element = current_element.parentNode
        elif separator == '+':
            current_element = current_element
        elif separator == '>':
            current_element = element

    return root

def decode(tree):
    """Takes a parsed tree and generates the HTML.
    """

    result = ''

    for subtree in tree.childNodes:
        result += subtree.toxml()

    return result

def embiggen(line):
    """Takes a line, parses it, and returns the generated HTML as a string.
    """

    return decode(parse(line))

def main():
    """Reads from `stdin` and generates the embiggened HTML for each line.
    """
    for line in sys.stdin:
        print embiggen(line)

if __name__ == "__main__":
    main()
