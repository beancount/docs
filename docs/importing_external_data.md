# Importing External Data in Beancount<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca), [<u>Moritz Lell</u>](mailto:mlell08@gmail.com), 2026

[<u>http://furius.ca/beancount/doc/beangulp</u>](http://furius.ca/beancount/doc/beangulp)

## Introduction<a id="introduction"></a>

This is the user’s manual for the library and tools in Beancount which can help you **automate the importing of external transaction data** into your Beancount input file and manage the documents you download from your financial institutions’ websites.

## Quickstart<a id="quickstart"></a>

To create an importer follow these steps.

1.  Create a python file “import.py”. More info in the Configuration section.

2.  Define importer(s) in the importers directory. More details in section Writing an importer.

3.  Put the .csv/.xml/.pdf file from your financial institution in the downloads directory. For more details, see section Organizing your files.

4.  Run uv run python import.py extract ./downloads &gt; tmp.beancount

There are examples in the [<u>beangulp repository</u>](https://github.com/beancount/beangulp/tree/master/examples/) and in the section “Writing an Importer”.

## The Importing Process<a id="the-importing-process"></a>

People often wonder how we do this, so let me describe candidly and in more detail what we’re talking about doing here.

The essence of the task at hand is to transcribe the transactions that occur in a person’s entire set of accounts to a single text file: the Beancount input file. Having the entire set of transactions ingested in a single system is what we need to do in order to generate comprehensive reports about one’s wealth and expenses. Some people call this “reconciling”.

We could transcribe all the transactions manually from paper statements by typing them in. However nowadays most financial institutions have a website where you can download a statement of historical transactions in a number of data formats which you can parse to output Beancount syntax for them.

Importing transactions from these documents involves:

-   Manually reviewing the transactions for **correctness** or even fraud;

-   **Merging** new transactions with previous transactions imported from another account. For example, a payment from a bank account to pay off one’s credit card will typically be imported from both the bank AND the credit card account. You must manually merge the corresponding transactions together[^1].

-   Assigning the right **category** to an expense transaction

-   **Organizing** your file by moving the resulting directives to the right place in your file.

-   **Verifying balances** either visually or inserting a Balance directive which asserts what the final account balance should be after the new transactions are inserted.

If my importers work without bugs, this is a process that takes me 30-60 minutes to update the majority of my active accounts. Less active accounts are updated every quarter or when I feel like it. I tend to do this on Saturday morning maybe twice per month, or sometimes weekly. If you maintain a well-organized input file with lots of assertions, mismatches are easily found, it’s a pleasant and easy process, and after you’re done generating an updated balance sheet is rewarding (I typically re-export to a Google Finance portfolio).

### Typical Downloads<a id="typical-downloads"></a>

Here’s a description of the typical kinds of files involved; this describes my use case and what I’ve managed to do. This should give you a qualitative sense of what’s involved.

-   **Credit cards and banks** provide fairly good quality historical statement downloads in OFX or CSV file formats but I need to categorize the other side of those transactions manually and merge some of the transactions together.

-   **Investment accounts** provide me with great quality of processable statements and the extraction of purchase transactions is fully automated, but I need to manually edit sales transactions in order to associate the correct cost basis. Some institutions for specialized products (e.g., P2P lending) provide only PDF files and those are translated manually.

-   **Payroll stubs and vesting events** are usually provided only as PDFs and I don't bother trying to extract data automatically; I transcribe those manually, keeping the input very regular and with postings in the same order as they appear on the statements. This makes it easier.

-   **Cash transactions**: I have to enter those by hand. I only book non-food expenses as individual transactions directly, and for food maybe once every six months I'll count my wallet balance and insert a summarizing transaction for each month to debit away the cash account towards food to make it balance. If you do this, you end up with surprisingly little transactions to type manually, maybe just a few each week (it depends on lifestyle choices, for me this works). When I’m on the go, I just note those on my phone in Google Keep and eventually transcribe them after they accumulate.

## Import Configuration<a id="import-configuration"></a>

To import the file contents into your Beancount ledger, you must create an *import configuration*. This is a regular Python file, which calls up an *Importer* that can process the file format. If you execute this file:

-   Each configured importer will test the input file whether it can handle it

-   If any Importer matches the file, it will convert its contents into beancount statements for your ledger, or move the file into your archive. You can choose the action via the command line arguments.

### Quick start: A minimal CSV import configuration<a id="quick-start-a-minimal-csv-import-configuration"></a>

Given you want to import the following CSV file with account statements, which you have downloaded from your bank:

    "Date";"Amount";"Purpose";"Balance after"
    2017-02-14;"-100,00";" BANKOMAT  00000483 K2 UM 11:56";"4.467,89"
    2017-02-13;"-50,00";"Payment to Company XYZ";"4.567,89"

This CSV file has “;” as column separator and “,” as decimal separator. Lets say for simplicity, that you always call your download “mybank.csv”. These characteristics must be specified in the importer, as well as the column name mapping. This is the importer configuration, which you save as “import.py”:

⎯⎯⎯ import.py ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

    import csv
    import beangulp  # Importing tools
    from beangulp.importers import csvbase
    class MyCSVImporter(csvbase.Importer):
        date = csvbase.Date("Date", "%Y-%m-%d")
        narration = csvbase.Column("Purpose")
        amount = csvbase.Amount("Amount", subs={r",": "."})
        balance = csvbase.Amount("Balance after", subs={r",": "."}) # optional
        order = csvbase.Order.DESCENDING # optional
        dialect = csv.excel
        dialect.delimiter = ";"
        def identify(self, filepath: str) -> bool:
            "Return True if this importer is suitable for the given filename."
            return filepath.endswith("mybank.csv")
    # List all available importers, one for each file format you need to process
    CONFIG = [
          # Default account name is applied if account column is undefined or empty
    MyCSVImporter(account="Assets:MyBank", currency="EUR")
    ]
    # Hooks: Process beancount transaction objects after they have been extracted
    HOOKS = []
    # Allows to call this script as './import extract <filename.csv>'.
    if __name__ == "__main__":
        ingest = beangulp.Ingest(CONFIG, HOOKS)
        ingest()

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ (END) ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

Call the script as “`python import.py --help`” to see the options:

-   “`python import.py extract mybank.csv >> new.beancount`” :  
    Convert to beancount statements and append to a beancount file of your choice

-   “`python import.py archive mybank.csv` “:  
    Move the file to the subfolder Assets/MyBank/2017-01-14.mybank.csv, that is, it will:

    -   Choose the subfolder based on the configured account

    -   Choose the prefix based on the last transaction

This example will produce a beancount transaction for each input CSV line. However, it will have only one posting (to your bank account). You will have to manually add the second posting (or multiple), for example to income or expense accounts before you have a valid transaction. If you want to automate this, you will need to overload the finalize() function as explained in the section “How to write a CSV importer”.

If you are using the graphical user interface for Beancount, Fava, make sure that the variables CONFIG and HOOKS are present in the script by these names, as Fava expects those two names to be present.

## Writing an Importer<a id="writing-an-importer"></a>

You have seen in the Quick Start section that an Importer for Beancount is a regular Python class in a regular Python module, which you execute to process your input file. Here, “processing” means two distinct steps:

a\) It can produce an output of Beancount statements from the input file which you will append to your Beancount Ledger

b\) It can move the file into your document folder, in the subfolder &lt;account&gt;/&lt;subaccount&gt;/&lt;date&gt;\_&lt;original-file-name&gt;.

These two functions are executed by calling the `extract` or `archive` command, respectively, as shown in the Quick Start section.

The Quick Start section, however, presents a special case: The import from a CSV file. There are multiple other formats, e.g. XML-based like CAMT, the older MF940, or even PDF files which require custom logic to parse. For all of these formats you can write Beancount Importers by writing subclasses of `beangulp.Importer`. This is detailed in the next section. The special case of CSV parsing follows afterwards.

### The importer protocol: Writing an importer for any file format<a id="the-importer-protocol-writing-an-importer-for-any-file-format"></a>

All importers must comply with a particular protocol and implement at least its required methods (identify() and account()). The full detail of this protocol is best found in the source code itself: [<u>importer.py</u>](https://github.com/beancount/beangulp/blob/master/beangulp/importer.py). The tools above will take care of finding the downloads and invoking the appropriate methods on your importer objects.

Here’s a brief summary of the methods (I have omitted the first ‘self’ argument for brevity)::

-   identify(filepath): This method just returns true if this importer can handle the given file name. All further tools invoke this function to figure out the list of (file, importer) pairs. Your importer must implement this method.

-   account(filepath): The account is used to determine the archival folder for the document. While the interface allows returning different accounts for different documents, normally the returned account name is just a constant for an importer subclass. Your importer must implement this method.

<!-- -->

-   extract(filepath, existing_entries): Extract some Beancount directives from the file contents. This method receives the file path (string) and the list of all existing beancount directives. It must create the new directives by instantiating the objects defined in beancount.core.data and return them as a list. If you don’t implement this method, your importer will not create any beancount statements and will only move your file to your documents folder.

-   name(filepath): This method provides a unique id for each importer instance. It’s convenient to be able to refer to your importers with a unique name; it gets printed out by the identification process, for instance. If you don’t define this method in your importer, a default name will be generated.

The following functions are related to archiving of the downloaded file in your documents folder after the import:

-   date(filepath): If a date can be extracted from the statement’s contents, return it here. This is useful for dated PDF statements… it’s often possible using regular expressions to grep out the date from a PDF converted to text. This allows the filing script to prepend a relevant date instead of using the date when the file was downloaded (the default).

-   filename(filepath): It’s most convenient not to bother renaming downloaded files. Oftentimes, the files generated from your bank either all have a unique name and they end up getting renamed by your browser when you download multiple ones and the names collide. This function is used for the importer to provide a “nice” name to file the download under.

-   You can overwrite two further functions, **`sort(...)`** and **`deduplicate(...)`**, however, the default implementations will probably be sufficient in most cases.

Use the final code lines as shown in the Quick Start section to create an executable Python script which will identify the correct importer for a given file. You can use  
`./your-import-script.py --help`  
to find out how to execute the import script.

It’s a good idea to write your importers as generically as possible and to parameterize them with the particular account names you use in your input file. This helps keep your code independent of the particular accounts and forces you to define logical accounts, and I’ve found that this helps with clarity.

Or not… At the end of the day, these importer codes live in some of your own personal place, not with Beancount. If you so desire, you can keep them as specific, or messy and unshareable as you like.

### Special Case: Writing a CSV importer <a id="special-case-writing-a-csv-importer"></a>

If you are importing from a CSV file, there is no need to re-implement the logic of CSV file parsing in your Importer, as the beangulp project has a generic CSV importer: `beangulp.importers.csvbase.Importer`. We will abbreviate the module name as “`csvbase`” in the following. The class `csvbase.Importer` implements all methods of the Importer protocol except “identify()”. It has its own Metaclass which allows you to define the CSV column names as simple member variables. This way, your own Importer subclass can be almost completely declarative.

Write your subclass of `csvbase.Importer` like this:

-   Implement the method **`identify(self, filename)`**, like explained in the previous section, to return True if your Importer can handle a given file.

-   Define class members which are of type `csvbase.Column` or its subclasses to define the column mapping:  
    `<beancount-name> = csvbase.Column_or_Subclass(“<Column name in CSV>”)`

    -   Mandatory names: date, narration, amount

    -   Optional names: flag, payee, account, currency, tag, link, balance. They fill the respective parts of a beancount directive. If you specify a balance column, a Balance assertion will be auto-generated after the last imported transaction.

    -   All other class members of type csvbase.Column or subclasses define additional data which is available to user-defined post-processing functions. These functions receive a named tuple (parameter “row”) of values for each line of the input CSV file. For example, you can add column contents as custom metadata to your transactions or postings in this way. See the subsection “Further customizations”.

-   The Column types can be:

    -   csvbase.Column(*names, default = None): The column value is taken verbatim as string, with an optional default if the value is empty

    -   csvbase.Columns(*names, …, sep = ‘ ‘): Merge multiple columns using ‘sep’

    -   csvbase.Date(name, frmt = ‘%Y-%m-%d’): Parse values as dates of given format

    -   csvbase.Amount(name, subs = {}): Parse values as numbers. To replace characters, the ‘subs’ dict can be used: { ‘regex1’: ‘replacement1’, ‘regex2’: ‘replacement2’, …}. For example, to parse a number like ‘1.000,00 EUR’, use 
                subs = {r”\.”: “”, r”,”: “.”, r” EUR”: “”}, 
            to replace first the dot by nothing, then the comma by a dot, and then the “ EUR” to nothing. This turns the number into “1000.00”, which Python can parse.

    -   csvbase.CreditOrDebit(credit, debit, subs = {}, default = None): Create a single amount from two colums, in which Credit (addition to account) and Debit (subtraction from account) are listed separately as positive numbers.

-   Define the format of the CSV file by overriding the members of `csvbase.CSVReader` (one of the two superclasses of `csvbase.Importer`). The options as of beangulp 0.2.0 are (with defaults):

    -   dialect (required) : The CSV dialect used in the input file, same as the argument to csv.Reader() of the same name.

    -   encoding = "utf8" : File encoding

    -   header = 0  : Number of header lines to skip.

    -   footer = 0 : Number of footer lines to ignore.

    -   names = True : Whether the data file contains a row with column names.

    -   comments = "#" : Comment character. Lines starting with this character are skipped.

    -   order = None. Order of entries in the CSV file. If None the order will be inferred from the file content. Use csvbase.Order.ASCENDING or ….DESCENDING.

As shown in the Quick Start section, you need to provide an instance of your importer subclass to `beangulp.Ingest`. Your CSV importer subclass inherits a constructor with the arguments `(account, currency, flag = “*”)`. You can either use that one (like in the Quick Start example) or provide your own `__init__` function which calls `super().__init__(account=…, currency=…, …)`.

#### Further customizations<a id="further-customizations"></a>

To customize the parsing of the CSV file, you can override the following methods. Besides, you can of course override all methods which were presented in the section “Writing an Importer”, however, this will require to re-implement some of the logic which is done by csvbase.Importer and csvbase.CSVReader.

-   metadata(filepath: str, lineno: int, row: Row) -> Meta
        This is called for each parsed transaction and you can add metadata

-   finalize(txn: Transaction, row: Row) -> Transaction 
        This method is called for each generated beancount  transaction object  and allows you to customize it. It is expected to return the modified object or None, which will skip this transaction.

The type annotations provide guidance on the expected input and output:

-   Meta: Create an object of this type using the function 
              new_metadata(filename, lineno, kvlist)
        from the module beancount.core.data. Typically, you will forward the first two parameters from the parameter list of the metadata(...) function. The third argument is your custom metadata as a dict object with string keys.

-   Row: This is a named tuple object which represents the data of a single CSV row. It will have an element for each member variable of your Importer subclass that is of type csvbase.Column or subclasses. Beyond the required and optional members like date, amount, … (see above), you can create further class members of any name corresponding to any CSV column and their data will be available in this object.

-   Transaction: This object is the internal Beancount representation of a transaction. Like all other Beancount directives, it is defined in the module beancount.core.data as a named tuple. Some elements which might be interesting for custom post-processing are payee, narration, meta (a dict) and postings (the list of Postings). Note that as a named tuple, it is an immutable object. To change some of its fields, use its _replace() method or the module ‘copy‘ to create an updated Transaction object. It is recommended to follow this pattern also for the mutable elements like the metadata and the list of postings.

## Hook functions<a id="hook-functions"></a>

The second argument to `beangulp.Ingest()` besides the importers is a list of hook functions. Hook functions are applied to all imported transactions. A hook function looks similar to this:

**def** my\_hook\_function(new\_entries\_list, existing\_entries):

out = \[\]

**for** filename, entries, account, importer **in** new\_entries\_list

modified\_entries = \[\]

**for** entry in entries:

\# ... ‘entry’ is of type beancount.core.data.Directive

\# ... Post-process the entries here...

\# ...

modified\_entries.append(entry)

out.append( (filename, modified\_entries, account, importer) )

**return** out

The argument new\_entries\_list is itself a list of tuples, with one element for each input file. Each tuple has as elements the input file name, the list of entries returned by the importer, the account and the importer object.

The element existing\_entries is a list of objects of type beancount.core.data.Directive and has all entries of the ledger before the import. This way, information from the ledger is available, for example for deduplication or to implement modification by machine learning.

## Further topics<a id="further-topics"></a>

### Configuring from an Input File<a id="configuring-from-an-input-file"></a>

An interesting idea that I haven’t tested yet is to use one’s Beancount input file to infer the configuration of importers. If you want to try this out and hack something, you can load your input file from the import configuration Python config, by using the API’s `beancount.loader.load_file()` function.

### Automating Network Downloads<a id="automating-network-downloads"></a>

The downloading of files is not something I automate, and Beancount provides no tools to connect to the network and fetch your files. There is simply too great a variety of protocols out there to make a meaningful contribution to this problem[^2]. Given the nature of today's secure websites and the castles of JavaScript used to implement them, it would be a nightmare to implement. Web scraping is probably too much to be a worthwhile, viable solution.

I **manually** log into the various websites with my usernames & passwords and click the right buttons to generate the downloaded files I need. These files are recognized automatically by the importers and extracting transactions and filing the documents in a well-organized directory hierarchy is automated using the tools described in this document.

While I’m not scripting the fetching, I think it’s possible to do so on some sites. That work is left for you to implement where you think it’s worth the time.

### Extracting Data from PDF Files<a id="extracting-data-from-pdf-files"></a>

I've made some headway toward converting data from PDF files, which is a common need, but it's incomplete; it turns out that fully automating table extraction from PDF isn't easy in the general case. I have some code that is close to working and will release it when the time is right. Otherwise, the best FOSS solution I’ve found for this is a tool called [<u>TabulaPDF</u>](http://tabula.technology/) but you still need to manually identify where the tables of data are located on the page; you may be able to automate some fetching using its sister project [<u>tabula-java</u>](https://github.com/tabulapdf/tabula-java).

Nevertheless, I usually have good success with my importers grepping around PDF statements converted to ugly text in order to identify what institution they are for and extracting the date of issuance of the document.

Finally, there are a number of different tools used to extract text from PDF documents, such as [<u>PDFMiner</u>](https://pypi.python.org/pypi/pdfminer2), [<u>LibreOffice</u>](https://www.libreoffice.org), the [<u>xpdf</u>](http://www.tutorialspoint.com/unix_commands/pdftotext.htm) library, the [<u>poppler</u>](https://poppler.freedesktop.org/) library[^3] and more... but none of them works consistently on all input documents; you will likely end up installing many and relying on different ones for different input files. For this reason, I’m not requiring a dependency on PDF conversion tools from within Beancount. You should test what works on your specific documents and invoke those tools from your importer implementations.

### Regression Testing your Importers<a id="regression-testing-your-importers"></a>

I've found over time that regression testing is *key* to maintaining your importer code working. Importers are often written against file formats with no official spec and unexpected surprises routinely occur. For example, I have XML files with some unescaped "&" characters, which require a custom fix just for that bank[^4]. I’ve also witnessed a discount brokerage switching its dates format between MM/DD/YY and DD/MM/YY; that importer now needs to be able to handle both types. So you make the necessary adjustment, and eventually you find out that something else breaks; this isn’t great. And the timing is particularly annoying: usually things break when you’re trying to update your ledger: you have other things to do.

The easiest, laziest and most relevant way to test those importers is to use some **real data files** and compare what your importer extracts from them to expected outputs. For the importers to be at least somewhat reliable, you really need to be able to reproduce the extractions on a number of real inputs. And since the inputs are so unpredictable and poorly defined, it’s not practical to write exhaustive tests on what they could be. In practice, I have to make at least *some* fix to *some* of my importers every couple of months, and with this process, it only sinks about a half-hour of my time: I add the new downloaded file which causes breakage to the importer directory, I fix the code by running it there locally as a test. And I also run the tests over *all* the previously downloaded test inputs in that directory (old and new) to ensure my importer is still working as intended on the older files.

There is some support for automating this process in [<u>beancount.ingest.regression</u>](https://github.com/beancount/beancount/tree/master/beancount/ingest/regression.py). What we want is some routine that will list the importer’s package directory, identify the input files which are to be used for testing, and generate a suite of unit tests which compares the output produced by importer methods to the contents of “expected files” placed next to the test file.

For example, given a package with an implementation of an importer and two sample input files:

    /home/joe/importers/acmebank/__init__.py   <- code goes here
    /home/joe/importers/acmebank/sample1.csv
    /home/joe/importers/acmebank/sample2.csv

You can place this code in the Python module (the \_\_init\_\_.py file):

    from beancount.ingest import regression
    …
    def test():
        importer = Importer(...)
        yield from regression.compare_sample_files(importer)

If your importer overrides the `extract()` and `file_date()` methods, this will generate four unit tests which get run automatically by [<u>pytest</u>](https://docs.pytest.org/en/latest/):

1.  A test which calls extract() on `sample1.csv`, prints the extracted entries to a string, and compares this string with the contents of sample1.csv.extract

2.  A test which calls `file_date()` on `sample1.csv` and compares the date with the one found in the `sample1.csv.file_date` file.

3.  A test like (1) but on `sample2.csv`

4.  A test like (2) but on `sample2.csv`

#### Generating Test Input<a id="generating-test-input"></a>

At first, the files containing the expected outputs do not exist. When an expected output file is absent like this, the regression tests automatically generate those files from the extracted output. This would result in the following list of files:

    /home/joe/importers/acmebank/__init__.py   <- code goes here
    /home/joe/importers/acmebank/sample1.csv
    /home/joe/importers/acmebank/sample1.csv.extract
    /home/joe/importers/acmebank/sample1.csv.file_date
    /home/joe/importers/acmebank/sample2.csv
    /home/joe/importers/acmebank/sample2.csv.extract
    /home/joe/importers/acmebank/sample2.csv.file_date

You should inspect the contents of the expected output files to visually assert that they represent the contents of the downloaded files.

If you run the tests again with those files present, the expected output files will be used as inputs to the tests. If the contents differ in the future, the test will fail and an error will be generated. (You can test this out now if you want, by manually editing and inserting some unexpected data in one of those files.)

When you edit your source code, you can always re-run the tests to make sure it still works on those older files. When a newly downloaded file fails, you repeat the process above: You make a copy of it in that directory, fix the importer, run it, check the expected files. That’s it[^5].

#### Making Incremental Improvements<a id="making-incremental-improvements"></a>

Sometimes I make improvements to the importers that result in more or better output being generated even in the older files, so that all the old tests will now fail. A good way to deal with this is to keep all of these files under source control, locally delete all the expected files, run the tests to regenerate new ones, and then diff against the most recent commit to check that the changes are as expected.

### Caching Data<a id="caching-data"></a>

Some of the data conversions for binary files can be costly and slow. This is usually the case for converting PDF files to text[^6]. This is particularly painful, since in the process of ingesting our downloaded data we’re typically going to run the tools multiple times—at least twice if everything works without flaw: once to extract, twice to file—and usually many more times if there are problems. For this reason, we want to cache these conversions, so that a painful 40 second PDF-to-text conversion doesn’t have to be run twice, for example.

Beancount aims to provide two levels of caching for conversions on downloaded files:

1.  An in-memory caching of conversions so that multiple importers requesting the same conversion runs them only once, and

2.  An on-disk caching of conversions so that multiple invocations of the tools get reused.

#### In-Memory Caching<a id="in-memory-caching"></a>

In-memory caching works like this: Your methods receive a wrapper object for a given file and invoke the wrapper’s `convert()` method, providing a converter callable/function.

    class MyImporter(ImporterProtocol):
        ...
        def extract(self, file):
            text = file.convert(slow_convert_pdf_to_text)
            match = re.search(..., text)

This conversion is automatically memoized: if two importers or two different methods use the same converter on the file, the conversion is only run once. This is a simple way of handling redundant conversions in-memory. Make sure to always call those through the `.convert()` method and share the converter functions to take advantage of this.

#### On-Disk Caching<a id="on-disk-caching"></a>

At the moment. Beancount only implements (1). On-disk caching will be implemented later. *Track this [<u>ticket</u>](https://github.com/beancount/beancount/issues/113) for status updates.*

## Organizing your Files<a id="organizing-your-files"></a>

The tools described in this document are pretty flexible in terms of letting you specify

-   **Import configuration**: The Python file which provides the list of importer objects as a configuration;

-   **Importers implementation**: The Python modules which implement the individual importers and their regression testing files;

-   **Downloads directory**: Which directory the downloaded files are to be found in;

-   **Filing directory**: Which directory the downloaded files are intended to be filed to.

You can specify these from any location you want. Despite this, some people are often asking how to organize their files, so I provide a template example under `beancount/examples/ingest/office`, and I describe this here.

I recommend that you create a Git or Mercurial[^7] source-controlled repository following this structure:

    office
    ├── documents
    │   ├── Assets
    │   ├── Liabilities
    │   ├── Income
    │   └── Expenses
    ├── importers
    │   ├── __init__.py
    │   └── … 
    │       ├── __init__.py
    │       ├── sample-download-1.csv
    │       ├── sample-download-1.extract
    │       ├── sample-download-1.file_date
    │       └── sample-download-1.file_name
    ├── personal.beancount
    └── personal.import

The root “office” directory is your repository. It contains your ledger file (“`personal.beancount`”), your importer configuration (“`personal.import`”), your custom importers source code (“`importers/`”) and your history of documents (“`documents/`”), which should be well-organized by bean-file. You always run the commands from this root directory.

An advantage of storing your documents in the same repository as your importers source code is that you can just symlink your regression tests to some files under the `documents/` directory.

You can check your configuration by running identify:

    python import.py identify ~/Downloads

If it works, you can extract transactions from your downloaded files at once:

    python import.py extract -e example.beancount~/Downloads > tmp.beancount

You then open tmp.beancount and move its contents to your personal.beancount file.

Once you’re finished, you can stash away the downloaded files for posterity like this:

    python import.py archive ~/Downloads -o documents

If my importers work, I usually don’t even bother opening those files. You can use the `--dry-run` option to test moving destinations before doing so.

To run the regression tests of the custom importers, use the following command:

    pytest -v importers

Personally, I have a `Makefile` in my root directory with these targets to make my life easier. Note that you will have to install “pytest”, which is a test runner; it is often packaged as “python3-pytest” or “pytest”.

## Example Importers<a id="example-importers"></a>

Beyond the documentation above, I cooked up an example importer for a made-up CSV file format for a made-up investment account. See [<u>this directory</u>](https://github.com/beancount/beangulp/blob/master/examples/importers/utrade.py).

There’s also an example of an importer which uses an external tool (PDFMiner2) to convert a PDF file to text to identify it and to extract the statement date from it. See [<u>this directory</u>](https://github.com/beancount/beancount/tree/master/examples/ingest/office/importers/acme/).

Beancount also comes with some very basic generic importers. See [<u>this directory</u>](https://github.com/beancount/beancount/tree/master/beancount/ingest/importers/).

-   There is a simple OFX importer that has worked for me for a long time. Though it’s pretty simple, I’ve used it for years, it’s good enough to pull info out of most credit card accounts.

-   There are also a couple of mixin classes you can mix into your importer implementation to make it more convenient; these are relics from the LedgerHub project—you don’t really need to use them—which can help in the transition to it.

Eventually I plan to build and provide a generic CSV file parser in this framework, as well as a parser for QIF files which should allow one to transition from Quicken to Beancount. (I need example inputs to do this; if you’re comfortable sharing your file I could use it to build this, as I don’t have any real input, I don’t use Quicken.) It would also be nice to build a converter from GnuCash at some point; this would go here as well.

## Cleaning Up<a id="cleaning-up"></a>

### Automatic Categorization<a id="automatic-categorization"></a>

A frequently asked question and common idea from first-time users is “How do I automatically assign a category to transactions I’ve imported which have only one side?” For example, importing transactions from a credit card account usually provides only one posting, like this:

    2016-03-18 * "UNION MARKET"
      Liabilities:US:CreditCard    -12.99 USD

For which you must manually insert an Expenses posting, like this:

    2016-03-18 * "UNION MARKET"
      Liabilities:US:CreditCard    -12.99 USD
      Expenses:Food:Grocery

People often have the impression that it is time-consuming to do this.

My standard answer is that while it would be fun to have, if you have a text editor with account name completion configured properly, it’s a breeze to do this manually and you don’t really need it. You wouldn’t save much time by automating this away. And personally I like to go over each of the transactions to check what they are and sometimes add comments (e.g., who I had dinner with, what that Amazon charge was for, etc.) and that’s when I categorize.

It’s something that could eventually be solved by letting the user provide some simple rules, or by using the history of past transactions to feed into a simple learning classifier.

*Beancount does not currently provide a mechanism to automatically categorize transactions. You can build this into your importer code. I want to provide a hook for the user to register a completion function that could run across all the importers where you could hook that code in.*

### Cleaning up Payees<a id="cleaning-up-payees"></a>

The payees that one can find in the downloads are usually ugly names:

-   They are sometimes the legal names of the business, which often does not reflect the street name of the place you went, for various reasons. For example, I recently ate at a restaurant called the “Lucky Bee” in New York, and the memo from the OFX file was “KING BEE”.

-   The names are sometimes abbreviation or contain some crud. In the previous example, the actual memo was “KING BEE NEW YO”, where “NEW YO” is a truncated location string.

-   The amount of ugliness is inconsistent between data sources.

It would be nice to be able to normalize the payee names by translating them at import time. I think you can do most of it using some simple rules mapping regular expressions to names provided by the user. There’s really no good automated way to obtain the “clean name” of the payee.

*Beancount does not provide a hook for letting you do this this yet. It will eventually. You could also build a plugin to rename those accounts when loading your ledger. I’ll build that too—it’s easy and would result in much nicer output.*

## Future Work<a id="future-work"></a>

A list of things I’d really want to add, beyond fortifying what’s already there:

-   A generic, configurable CSV importer which you can instantiate. I plan to play with this a bit and build a sniffer that could automatically figure out the role of each column.

-   A hook to allow you to register a callback for post-processing transactions that works across all importers.

## Related Discussion Threads<a id="related-discussion-threads"></a>

-   [<u>Getting started; assigning accounts to bank .csv data</u>](https://groups.google.com/d/msg/ledger-cli/u648SA1o-Ek/DzZmu8wVCAAJ)

-   [<u>Status of LedgerHub… how can I get started?</u>](https://groups.google.com/d/msg/beancount/qFZvGBLuJos/WSaNY0sEc-wJ)

-   [<u>Rekon wants your CSV files</u>](https://groups.google.com/d/msg/ledger-cli/n_WNc-tZabU/sh09irl-C-kJ)

## Historical Notes<a id="historical-notes"></a>

There once was a first implementation of the process described in this document. The project was called LedgerHub and has been decommissioned in February 2016, rewritten and the resulting code integrated in Beancount itself, into this [<u>beancount.ingest</u>](https://github.com/beancount/beancount/tree/master/beancount/ingest/) library, which is now further moved to the beangulp project. The original project was intended to include the implementation of various importers to share them with other people, but this sharing was not very successful, and so the rewrite includes only the scaffolding for building your own importers and invoking them, and only a very limited number of example importer implementations.

Documents about LedgerHub are preserved, and can help you understand the origins and design choices for Beancount’s importer support. They can be found here:

-   [<u>Original design</u>](ledgerhub_design_doc.md)

-   [<u>Original instructions & final status</u>](http://furius.ca/beancount/doc/ledgerhub/manual) (the old version of this doc)

-   [<u>An analysis of the reasons why it the project was terminated</u>](http://furius.ca/beancount/doc/ledgerhub/postmortem) (post-mortem)

[^1]: There are essentially three conceptual modes of entering such transactions: (1) a user crafts a single transaction manually, (2) another where a user inputs the two sides as a single transaction to transfer accounts, and (3) the two separate transactions get merged into a single one automatically. These are dual modes of each other. The twist in this story is that the same transaction often posts at different dates in each of its accounts. Beancount currently \[March 2016\] does not support multiple dates for a single transaction’s postings, but a discussion is ongoing to implement support for these input modes. See [<u>this document</u>](settlement_dates_in_beancount.md) for more details.

[^2]: The closest to universal downloader you will find in the free software world is [<u>ofxclient</u>](https://github.com/captin411/ofxclient) for OFX files, and in the commercial world, [<u>Yodlee</u>](http://www.yodlee.com/) provides a service that connects to many financial institutions.

[^3]: The ‘pdftotext’ utility in poppler provides the useful ‘-layout’ flag which outputs a text file without mangling tables, which can be helpful in the normal case of ‘transaction-per-row’

[^4]: After sending them a few detailed emails about this and getting no response nor seeing any change in the downloaded files, I have given up on them fixing the issue.

[^5]: As you can see, this process is partly why I don’t share my importers code. It requires the storage of way too much personal data in order to keep them working.

[^6]: I don’t really understand why, since opening them up for viewing is almost instant, but nearly all the tools to convert them to other formats are vastly slower.

[^7]: I personally much prefer Mercurial for the clarity of its commands and output and its extensibility, but an advantage of Git’s storage model is that moving files within it comes for free (no extra copy is stored). Moving files in a Mercurial repository costs you a bit in storage space. And if you rename accounts or change how you organize your files you will end up potentially copying many large files.
