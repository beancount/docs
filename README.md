# Beancount Documentation

https://beancount.github.io/docs/

Source files are in [docs](docs/) directory.

These documents in markdown format are automatically generated from [official Beancount documentation](http://furius.ca/beancount/doc/index).

You [can contribute](CONTRIBUTING.md).

## Beancount Google Doc converter

### Installation

The converter requires python 3.6 - 3.10.

Create virtualenv (recommended):

```
python3 -m venv venv
. venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

### Usage

Export and convert single document:

```shell
# Export google document as docx file
python export.py document "100tGcA4blh6KSXPRGCZpUlyxaRUwFHEvnz_k9DyZFn4" doubleentry.docx
# Export drawings
python export.py drawings "100tGcA4blh6KSXPRGCZpUlyxaRUwFHEvnz_k9DyZFn4" drawings
# Convert docx file to markdown
python export.py convert doubleentry.docx doubleentry.md --drawing-dir=drawings
```

Export and convert all documents:

```
python crawl.py
```

## Documentation website

Generate static website using [Zensical](https://zensical.org/):

```
make serve
```

Build the static site:

```
make build
```
