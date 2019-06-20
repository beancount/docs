import argparse
import io

import requests
import pypandoc
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

INTERMEDIATE_FMT = 'docx'


def download_file(
    document_id: str,
    fmt=INTERMEDIATE_FMT,
    file_name=None,
) -> bytes:
    """
    Export and download. Formats available: docx, odt, rtf, txt
    https://googlesystem.blogspot.com/2007/07/download-published-documents-and.html
    """
    url = f'https://docs.google.com/document/export?format={fmt}&id={document_id}'
    response = requests.get(url)
    response.raise_for_status()
    if not file_name:
        file_name = f'document.{fmt}'
    with open(file_name, 'wb') as file:
        file.write(response.content)


def prepare_docx(file_name: str) -> bytes:
    """
    Add SourceCode style
    https://groups.google.com/d/msg/pandoc-discuss/SIwE9dhGF4U/Wjy8zmQ1CQAJ
    """
    doc = Document(file_name)
    doc.styles.add_style('SourceCode', WD_STYLE_TYPE.PARAGRAPH)
    for para in doc.paragraphs:
        if len(para.runs) == 0:
            continue
        if para.runs[0].font.name == 'Consolas':
            para.style = doc.styles['SourceCode']
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def convert(
    document: bytes,
    input_fmt: str = INTERMEDIATE_FMT,
    output_fmt: str = 'markdown_strict',
) -> str:
    """
    Equivalent to
    pandoc document.docx -f docx -t markdown_strict --standalone --wrap=none --filter filter.py
    """
    output = pypandoc.convert_text(
        document,
        output_fmt,
        format=input_fmt,
        extra_args=[
            '--wrap=none',  # Don't wrap lines
            '--standalone',  # Don't strip headers
        ],
        filters=[
            'filter.py',
        ],
    )
    return output


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    download_parser = subparsers.add_parser(
        'download',
        help='download document')
    download_parser.add_argument('id', help='document id')
    download_parser.add_argument('--name', help='file name')

    convert_parser = subparsers.add_parser(
        'convert',
        help='convert document')
    convert_parser.add_argument('name', help='docx file name')
    convert_parser.add_argument(
        '--format',
        help='output format',
        default='markdown_strict')
    args = parser.parse_args()

    if args.command == 'download':
        download_file(args.id, file_name=args.name)
    elif args.command == 'convert':
        document_path = args.name
        document = prepare_docx(document_path)
        result = convert(document, output_fmt=args.format)
        print(result)


if __name__ == '__main__':
    main()
