import json
import logging
import re

from panflute import (
    run_filter,
    stringify,
    BlockQuote,
    CodeBlock,
    Header,
    LineBreak,
    Link,
    ListItem,
    Para,
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
        response = requests.get(url, allow_redirects=True, stream=True)
        if any(res.status_code == 302 for res in response.history):
            url = response.url  # Final location
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
    if doc.get_metadata('title') is None:
        # No title -> Beancount Options Reference
        if isinstance(elem, Para):
            # Convert all paragraphs to code blocks
            text = stringify(elem)
            if not text.startswith('option'):
                text = '    ' + text
            return CodeBlock(text)
        # Skip everything else
        return

    if isinstance(elem, BlockQuote):
        if isinstance(elem.parent, ListItem):
            # Don't use blockquotes in lists
            assert len(elem.content) == 1
            return elem.content[0]
        elif any(isinstance(item, CodeBlock) for item in elem.content):
            # Remove blockquotes around code blocks
            return [item for item in elem.content]
        elif len(elem.content) == 1:
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

    elif isinstance(elem, CodeBlock):
        # Remove unnecessary leading tabs from code blocks
        elem.text = re.sub(r'^\t', '', elem.text, flags=re.MULTILINE)


def main(doc=None):
    return run_filter(action, prepare=prepare, doc=doc)


if __name__ == '__main__':
    main()
