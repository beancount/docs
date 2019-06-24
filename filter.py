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


def main(doc=None):
    return run_filter(action, prepare=prepare, doc=doc)


if __name__ == '__main__':
    main()
