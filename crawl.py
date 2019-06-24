import re
import os
import tempfile

from bs4 import BeautifulSoup
from slugify import slugify

from export import download_file, prepare_docx, convert

INDEX_DOCUMENT_ID = '1RaondTJCS_IUPBHFNdT8oqFKJjVJDsfsn6JEjBG04eA'


def main():
    # Find all Google Docs links in documentation index
    index_html = download_file(INDEX_DOCUMENT_ID, fmt='html')
    soup = BeautifulSoup(index_html, 'lxml')
    results = {INDEX_DOCUMENT_ID: 'Beancount Documentation'}
    for elem in soup.find_all('a'):
        match = re.search(r'document/d/([\w-]+)[/&]', elem['href'])
        if not match:
            continue
        document_id = match.group(1)
        if document_id in results:
            continue
        document_title = elem.get_text()
        if document_title == 'H':
            # Bad markup here
            document_title = 'How Inventories Work'
        results[document_id] = document_title
    print(f'Found {len(results)} documents')

    # Export and convert all found documents
    for idx, (document_id, document_title) in enumerate(results.items()):
        print(f'Processing "{document_title}"')
        with tempfile.NamedTemporaryFile() as temp_file:
            download_file(document_id, file_name=temp_file.name)
            document = prepare_docx(temp_file.name)
        document_slug = slugify(document_title, separator='_')
        output_path = os.path.join('docs', f'{idx:02d}_{document_slug}.md')
        output = convert(document)
        with open(output_path, 'w') as output_file:
            output_file.write(output)

    print('Done.')


if __name__ == '__main__':
    main()
