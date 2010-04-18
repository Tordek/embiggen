#!/usr/bin/env python

"""Embiggen --- Simpler HTML.

Embiggen is a simple filter program that takes a CSS-like syntax, and
'embiggens' it, generating the corresponding HTML code.

Embiggen is under the 2-clause BSD license. See the COPYING file for details.

TODO: Multipliers.
TODO: Placeholders.
TODO: Command line options.
TODO: Shortcuts.
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

    required = {
        'a': {'href': ''},
        'base': {'href': ''},
        'abbr': {'title': ''},
        'acronym':{'title': ''},
        'bdo': {'dir': ''},
        'link': {'rel': 'stylesheet', 'href': ''},
        'style': {'type': 'text/css'},
        'script': {'type': 'text/javascript'},
        'img': {'src':'', 'alt':''},
        'iframe': {'src': '', 'frameborder': '0'},
        'embed': {'src': '', 'type': ''},
        'object': {'data': '', 'type': ''},
        'param': {'name': '', 'value': ''},
        'form': {'action': '', 'method': 'post'},
        'table': {'cellspacing': '0'},
        'input': {'type': '', 'name': '', 'value': ''},
        'base': {'href': ''},
        'area': {'shape': '', 'coords': '', 'href': '', 'alt': ''},
        'select': {'name': ''},
        'option': {'value': ''},
        'textarea':{'name': ''},
        'meta': {'content': ''},
    }

    result = re.match(r'\s*(\w+)'                     # Name
                      r'\s*(?:#(\w+))?'               # ID
                      r'((?:\s*\.\w+)*)'              # Classes
                      r'((?:\s*\[[^\]]+\])*)'         # Properties
                      r'(?:\s*\{(\s*[^\}]+)\s*\})?',  # Content
                      element_unparsed)

    name, id_, classes, properties, content = result.group(1, 2, 3, 4, 5)

    element = Element(name)

    if id_ is not None:
        element.setAttribute("id", id_)

    if classes is not None and classes != '':
        element.setAttribute("class",
                             ' '.join(re.split(r'\s*\.', classes)[1:]))

    if required.has_key(name):
        for property_name, property_value in required[name].iteritems():
            element.setAttribute(property_name, property_value)

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
    result = re.match(r'((?:\s*(?:[\.#]?\w+|\[[^\]]+\]|\{[^\}]+\}))+)'
                      r'\s*(?:(<|\+|>)(.*))?', line)
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

        if isinstance(current_element.lastChild, Text) and \
           current_element.lastChild.data == '':
            current_element.removeChild(current_element.lastChild)

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

def pretty_print(node, indent, addindent, newline):
    """Pretty-print an XML-tree.

    This pretty-printing function values human-readability more than pedantic
    HTML correctness. Many block nodes (like `p`) aren't rendered like others
    (with a newline after the opening tag, and indented contents).
    """
    if isinstance(node, Text):
        return indent + node.data + newline

    block_nodes = ['address', 'blockquote', 'div', 'dl', 'ul', 'ol',
                   'fieldset', 'form', 'tr', 'table', 'tbody', 'thead',
                   'tfoot', 'noframes', 'frameset']

    value = indent + '<' + node.tagName

    for attribute_name, attribute_value in sorted(node.attributes.items()):
        value += ' %s="%s"'%(attribute_name, attribute_value)

    # It's incredible I need the second test.
    if node.hasChildNodes and len(node.childNodes) > 0:
        value += '>'

        if node.tagName not in block_nodes and len(node.childNodes) == 1:
            value += pretty_print(node.childNodes[0], '', '', '')
        else:
            value += newline

            for child in node.childNodes:
                value += pretty_print(child, indent + addindent, addindent,
                                      newline)
                if value[-1] != newline:
                    value += newline

            value += indent

        value += '</' + node.tagName + '>'
    else:
        value += '/>'

    return value

def decode(tree, indent, newline):
    """Takes a parsed tree and generates the HTML.
    """

    result = ''

    for subtree in tree.childNodes:
        result += pretty_print(subtree, '', indent, newline) + newline

    return result

def embiggen(line, indent, newline):
    """Takes a line, parses it, and returns the generated HTML as a string.
    """

    return decode(parse(line), indent, newline)

def main():
    """Reads from `stdin` and generates the embiggened HTML for each line.
    """
    for line in sys.stdin:
        print embiggen(line, '\t', '\n')

if __name__ == "__main__":
    main()
