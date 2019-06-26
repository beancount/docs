import json
import logging

from panflute import (
    run_filter,
    stringify,
    BlockQuote,
    CodeBlock,
    Header,
    LineBreak,
    Link,
    ListItem,
    Space,
    Str,
)
import requests

from constants import GOOGLE_DOC_URL_REGEXP

logging.basicConfig(
    filename='filter.log',
    filemode='w',
    level=logging.INFO,
    format='%(message)s',
)


def prepare(doc):
    # Insert title
    title = doc.get_metadata('title')
    if title:
        title_elem = Header(Str(title), level=1, identifier='title')
        doc.content.insert(0, title_elem)


def resolve_url(url: str) -> str:
    if '//furius.ca' in url:
        # Get Google Doc url
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 302:
            url = response.headers['Location']
        else:
            # Not a redirect, leave as is
            return None
    match = GOOGLE_DOC_URL_REGEXP.search(url)
    if not match:
        # Not a Google Doc
        return None
    document_id = match.group(1)
    with open('index.json', 'r') as index_json:
        document_map = json.load(index_json)
    return document_map.get(document_id)


def action(elem, doc):
    if isinstance(elem, BlockQuote):
        if isinstance(elem.parent, ListItem):
            # Don't use blockquotes in lists
            return elem.content[0]
        elif isinstance(elem.content[0], CodeBlock):
            # Remove blockquotes from code blocks
            return elem.content[0]
        else:
            # Convert blockquotes to code blocks
            code = ''
            for item in elem.content[0].content:
                if isinstance(item, Link):
                    # Don't convert links to code
                    break
                elif isinstance(item, Str):
                    code += item.text
                elif isinstance(item, Space):
                    code += ' '
                elif isinstance(item, LineBreak):
                    code += '\n'
                else:
                    code += stringify(item)
            else:
                return CodeBlock(code)
    elif isinstance(elem, Header):
        # There must be only one level 1 header
        if elem.identifier != 'title':
            elem.level += 1
    elif isinstance(elem, Link):
        if elem.url == stringify(elem):
            # Displayed as url, skip
            pass
        else:
            resolved = resolve_url(elem.url)
            if resolved:
                elem.url = resolved


def main(doc=None):
    return run_filter(action, prepare=prepare, doc=doc)


if __name__ == '__main__':
    main()
