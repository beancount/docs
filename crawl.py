import json
import os
import tempfile

from bs4 import BeautifulSoup
from slugify import slugify

from constants import GOOGLE_DOC_INDEX_ID, GOOGLE_DOC_URL_REGEXP
from export import download_file, prepare_docx, convert


def get_index() -> dict:
    """
    Find all Google Docs links in documentation index
    """
    document_map = {GOOGLE_DOC_INDEX_ID: '00_beancount_documentation.md'}
    index_html = download_file(GOOGLE_DOC_INDEX_ID, fmt='html')
    soup = BeautifulSoup(index_html, 'lxml')
    for elem in soup.find_all('a'):
        match = GOOGLE_DOC_URL_REGEXP.search(elem['href'])
        if not match:
            continue
        document_id = match.group(1)
        if document_id in document_map:
            continue
        document_title = elem.get_text()
        if document_title == 'H':
            # Bad markup here
            document_title = 'How Inventories Work'
        document_slug = slugify(document_title, separator='_')
        filename = f'{len(document_map):02d}_{document_slug}.md'
        document_map[document_id] = filename

    with open('index.json', 'w') as index_json:
        json.dump(document_map, index_json, indent=4)

    print(f'Found {len(document_map)} documents')
    return document_map


def main():
    """
    Export and convert all found documents
    """
    documents = get_index()
    for document_id, filename in documents.items():
        print(f'Processing https://docs.google.com/document/d/{document_id}/')
        with tempfile.NamedTemporaryFile() as temp_file:
            download_file(document_id, file_name=temp_file.name)
            document = prepare_docx(temp_file.name)
        output_path = os.path.join('docs', filename)
        output = convert(document)
        with open(output_path, 'w') as output_file:
            output_file.write(output)

    print('Done.')


if __name__ == '__main__':
    main()
