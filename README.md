[Index](docs/00_beancount_documentation.md)

# Beancount Google Doc converter

## Requirements

* python 3
* pandoc

## Usage

Export and convert single document:

```
python export.py document "100tGcA4blh6KSXPRGCZpUlyxaRUwFHEvnz_k9DyZFn4" doubleentry.docx
python export.py drawings "100tGcA4blh6KSXPRGCZpUlyxaRUwFHEvnz_k9DyZFn4" drawings
python export.py convert doubleentry.docx doubleentry.md --drawing-dir=drawings
```

Export and convert all documents:

```
python crawl.py
```
