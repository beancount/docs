Design Doc for Ledgerhub<a id="title"></a>
==========================================

[<span class="underline">Martin Blais</span>](mailto:blais@furius.ca), February 2014

[<span class="underline">http://furius.ca/beancount/doc/ledgerhub-design-doc</span>](http://furius.ca/beancount/doc/ledgerhub-design-doc)

> [<span class="underline">Motivation</span>](#motivation)
>
> [<span class="underline">Goals & Stages</span>](#goals-stages)
>
> [<span class="underline">Details of Stages</span>](#details-of-stages)
>
> [<span class="underline">Fetching</span>](#fetching)
>
> [<span class="underline">Identification</span>](#identification)
>
> [<span class="underline">Extraction</span>](#extraction)
>
> [<span class="underline">Transform</span>](#transform)
>
> [<span class="underline">Rendering</span>](#rendering)
>
> [<span class="underline">Filing</span>](#filing)
>
> [<span class="underline">Implementation Details</span>](#implementation-details)
>
> [<span class="underline">Importers Interface</span>](#importers-interface)
>
> [<span class="underline">References</span>](#references)

***Please note that this document is the original design doc for LedgerHub. LedgerHub is being transitioned back to Beancount. See [<span class="underline">this postmortem document</span>](https://docs.google.com/document/d/1Bln8Zo11Cvez2rdEgpnM-oBHC1B6uPC18Qm7ulobolM/) for details \[blais, 2015-12\].***

Motivation<a id="motivation"></a>
---------------------------------

Several open source projects currently exist that provide the capability to create double-entry transactions for bookkeeping from a text file input. These various double-entry bookkeeping projects include [<span class="underline">Beancount</span>](http://furius.ca/beancount/), [<span class="underline">Ledger</span>](http://ledger-cli.org/), [<span class="underline">HLedger</span>](http://hledger.org/), [<span class="underline">Abandon</span>](https://github.com/hrj/abandon), and they are independent implementations of a similar goal: the creation of an in-memory representation for double-entry accounting transactions from a text file, and the production of various reports from it, such as balance sheets, income statements, journals, and others. Each implementation explores slightly different feature sets, but essentially all work by reading their input from a file whose format is custom declarative language that describe the transactions, a language which is meant to be written by humans and whose syntax is designed with that goal in mind. While the languages do vary somewhat, the underlying data structures that they define are fairly similar.

An essential part of the process of regularly updating one’s journal files is the replication of a real-world account’s transaction detail to a single input file in a consistent data format. This is essentially a translation step, meant to bring the transaction details of many institutions’ accounts into a single system. Various banks and credit card companies provide downloadable transaction data in either Quicken or Microsoft Money (OFX) formats, and many institutions provide custom CSV files with transaction detail. Moreover, many of these institutions also make regular statements available for download as PDF files, and these can be associated with one’s ledger accounts.

The process of translating these external data formats can be automated to some extent. These various files can be translated to output text that can then be massaged by the user to be integrated into input file formats accepted by a double-entry bookkeeping package. Several projects have begun to make inroads in that domain: [<span class="underline">Ledger-autosync</span>](https://pypi.python.org/pypi/ledger-autosync/) aims at fetching transactions automatically from OFX servers for and translating them for Ledger and HLedger, and [<span class="underline">Reckon</span>](https://github.com/cantino/reckon) converts CSV files for Ledger. [<span class="underline">Beancount</span>](http://furius.ca/beancount/) includes code that can automate the identification of downloaded files to the accounts from a ledger, extract their transaction detail, and automatically file them to a directory hierarchy that mirrors the ledger’s chart of accounts. This code should probably live outside of Beancount. [<span class="underline">Ledger</span>](http://ledger-cli.org/) also sports a “convert” command that attempts to do similar things and a [<span class="underline">CSV2Ledger</span>](https://github.com/jwiegley/CSV2Ledger) Perl script is available that can convert CSV files. HLedger also had a convert command which translated CSV files with optional conversion hints defined in a separate file; HLedger now [<span class="underline">does the same conversion on-the-fly when the input file is CSV</span>](http://hledger.org/manual#csv-files) (i.e., CSV is considered a first-class input format).

The programs that fetch and convert external data files do not have to be tied to a single system. Moreover, this is often cumbersome code that would benefit greatly from having a large number of contributors, which could each benefit each other from having common parsers ready and working for the various institutions that they’re using or likely to use in the future. I - the author of Beancount - have decided to move Beancount’s importing and filing source code outside of its home project and to decouple it from the Beancount source code, so that others can contribute to it, with the intent of providing project-agnostic functionality. This document describes the goals and design of this project.

Goals & Stages<a id="goals-stages"></a>
---------------------------------------

This new project should address the following aspects in a project-agnostic manner:

-   **Fetching**: Automate *obtaining* the external data files by connecting to the data sources directly. External tools and libraries such as [<span class="underline">ofxclient</span>](https://github.com/captin411/ofxclient) for OFX sources can be leveraged for this purpose. Web scraping could be used to fetch downloadable files where possible. The output of this stage is a list of institution-specific files downloaded to a directory.  
    Note that fetching does not just apply to transaction data here; we will also support fetching *prices*. A list of (date, price) entries may be created from this data. We will likely want to support an intermediate format for expressing a list of positions (and appropriate support in the ledgerhub-Ledger/Beancount/HLedger interface to obtain it).

-   **Identification**: Given a filename and its contents, automatically *guess* which institution and account configuration the file is for, and ideally be able to extract the date from the file or statement. This should also work with PDF files. The output of this stage is an association of each input file to a particular extractor and configuration (e.g. a particular account name).

-   **Extraction**: *Parse each file* (if possible) and extract a list of information required to generate double-entry transactions data structures from it, in some sort of *generic* data structure, such as dicts of strings and numbers, independent of the underlying project’s desired output. If possible, a verbatim snippet of the original text that generated the transaction should be attached to the output data structure. The output of this stage is a data structure, e.g., a list of Python dictionaries in some defined format.

-   **Transform**: Given some information from the past transaction history contained in a journal, using simple learning algorithms, a program should be able to apply transformations on the transactional information extracted from the previous step. The most common use case for this is to automatically add a categorization posting to transactions that have a single posting only. For example, transactions from credit card statements typically include the changes in balance of the credit card account but all transactions are left to be manually associated with a particular expense account. Some of this process can be automated at this stage.

<!-- -->

-   **Rendering**: Convert the internal transactions data structures to the particular syntax of a double-entry bookkeeping project implementation and to the particular desired syntax variants (e.g. currency formatting, comma vs. dot decimal separator, localized input date format). This steps spits out text to be inserted into an input file compatible with the ledger software of choice.

-   **Filing**: Sanitize the downloaded files’ filenames and move them into a well organized and structured directory hierarchy corresponding to the identified account. This can run from the same associations derived in the identification step.

Apart from the Render stage, all the other stages should be implemented without regard for a particular project, this should work across all ledger implementations. The Rendering code, however, should specialize, import source code, and attempt to add as many of the particular features provided by each project to its output text.

Where necessary, interfaces to obtain particular data sets from each ledger implementation’s input files should be provided to shield the common code from the particular implementation details of that project. For instance, a categorization Transform step would need to train its algorithm on some of the transaction data (i.e., the narration fields and perhaps some of the amounts, account names, and dates). Each project should provide a way to obtain the necessary data from its input data file, in the same format.

Details of Stages<a id="details-of-stages"></a>
-----------------------------------------------

### Fetching<a id="fetching"></a>

By default, a user should be able to click their way to their institution’s website and download documents to their ~/Downloads directory. A directory with some files in it should be the reasonable default input to the identification stage. This directory should be allowed to have other/garbage files in it, the identification step should be able to skip those automatically.

A module that can automatically fetch the data needs to be implemented. Ideally this would not require an external tool. The data extracted should also have a copy saved in some Downloads directory.

This is the domain of the ledger-autosync project. Perhaps we should coordinate input/outputs or even integrate call some of its library code at this stage. The author notes that fetching data from OFX servers is pretty easy, though the begin/end dates will have to get processed and filtered.

Automatic fetching support will vary widely depending on where the institutions are located. Some places have solid support, some less. Use the data from [<span class="underline">ofxhome.com</span>](http://ofxhome.com) to configure.

#### Fetching Prices<a id="fetching-prices"></a>

For fetching prices, there are many libraries out there. Initially we will port Beancount’s bean-prices to ledgerhub.

### Identification<a id="identification"></a>

The identification stage consists in running a driver program that

-   Searches for files in a directory hierarchy (typically your ~/Downloads folder)

-   If necessary, converts the files into some text/ascii format, so that regular expressions can be matched against it (even if the output is messy, e.g., with PDF files converted to ASCII). This works well for PDF files: despite the fact that we cannot typically extract transactional data from them, we can generally pretty reliably identify which account they’re for and almost always extract the statement date as well.

-   Check a list of regular expressions against the ASCII’fied contents. If the regular expressions all match, the configuration is associated to the filename.

Note that more than one configuration may be associated to the same file because some files contain many sections, sections for which different importers may be called on to extract their data (e.g., OFX banking + OFX credit card can be mixed in the same file, and some institutions do).

The net result of this process is an association of each filename with the a specific importer object instantiated in the configuration file. These importer objects are created with a set of required account names which they use to produce the Ledger-like syntax from the downloaded file that was associated with it. Here is an example configuration for two importers:

from ledgerhub.sources.rbc import rbcinvesting, rbcpdf

CONFIG = \[

...

(('FileType: application/vnd.ms-excel', r'Filename: .\*Activity-123456789-', ),  
rbcinvesting.Importer({  
'FILE' : 'Assets:CA:RBC-Investing:Taxable',  
'cash' : 'Assets:CA:RBC-Investing:Taxable:Cash',  
'positions' : 'Assets:CA:RBC-Investing:Taxable',  
'interest' : 'Income:CA:RBC-Investing:Taxable:Interest',  
'dividend' : 'Income:CA:RBC-Investing:Taxable:Dividends',  
'fees' : 'Expenses:Financial:Fees',  
'commission' : 'Expenses:Financial:Commissions',  
'transfer' : 'Assets:CA:RBC:Checking',  
})),  
  
(('FileType: application/pdf',  
'Filename:.\*/123456789-\\d\\d\\d\\d\[A-Z\]\[a-z\]\[a-z\]\\d\\d-\\d\\d\\d\\d\[A-Z\]\[a-z\]\[a-z\]\\d\\d.pdf'),  
rbcpdf.Importer({  
'FILE': 'Assets:CA:RBC-Investing:RRSP',  
})),

The configuration consists in a list, for each possible importer, of a pair of 1) a list of regular expressions which all should match against a “match text”, which is a “textified” version of the contents of a file to be imported, and 2) an importer object, configured with a specific set of accounts to use for producing transactions. Each importer requires a particular set of output accounts which it uses to create its transactions and postings. The ledger’s filename, and a list of these (regexps, importer) pairs is all that is necessary for the driver to carry out all of its work.

The textification consists in a simple and imperfect conversion of downloaded file that are in binary format to something that we can run regular expressions against. For an OFX file or CSV file there is no conversion required for textification, we can just match against the text contents of those files; for an Excel/XLS file, we need to convert that to a CSV file, which can then be searched; for a PDF file, a number of different pdf-to-text converters are attempted until one succeeds (the tools for this are notoriously unreliable, so we have to try various ones). Note that this converted "match text" is only created temporarily and only for the purpose of identification; the importer will get the original binary file to do its work.

It is not entirely clear whether the regular expressions can be standardized to avoid having the user configure them manually. In practice, I have found it often necessary, or at least very convenient, to place an account id in my import configuration. It is true that configuring each of the possible downloads can be a hassle that requires the user to do a bit of guesswork while looking at the contents of each file, but this has been much more reliable in practice than attempts at normalizing this process, likely because it is a much easier problem to uniquely distinguish between all the files of a particular user than to distinguish between all the types of files. Using an account id in one of the regular expressions is the easy way to do that, and it works well. This also provides a clear place to attach the list of accounts to a particular importer, something that necessarily requires user input anyway.

### Extraction<a id="extraction"></a>

Once the association is made, we run the importers on each of the files. Some data structure is produced. The importers each do what they do - this is where the ugly tricks go. Ideally, we should build a library of common utilities to help parsing similar file types.

Though each of the importer modules should be pretty much independent, some common functionality can be imagined, for example, how one deals with different stocks held in a single investment account, could be configured outside of each importer (e.g., preferred method could be to create a subaccount of that account, with the symbol of the stock, or otherwise).

Note \[AMaffei\]: This could output a generic and well-defined CSV file format if you want to have the option of running the various steps as separate UNIX-style tools and/or process the intermediate files with regular text processing tools.

### Transform<a id="transform"></a>

Some transformations should be independent of importers. In particular, automatically categorizing incomplete transactions is not dependent on which importer created the transaction. I’d like to keep this step as general as possible so that other embellishment steps can be inserted here in the future. Right now, I can only think of the following uses:

1.  Auto-categorization of transactions with only a single leg

2.  Detection of duplicate transactions: imported files often contain transactions which are already in the ledger; those should be either ignored or marked as such. In practice, this is not as easy as it sounds, because a straightforward date + narration comparison will fail: if the same transaction comes from two input data files, one side always ends up getting merged to the other, and sometimes even the date differs a bit. Some amount of fuzzy matching is required.

3.  Normalization of payee names: the imported names of payees are often cut short or include some irrelevant words, such as “LLC”, city names, and/or number codes. It may be desirable to somehow clean those up automatically.

This step involves a bootstrapping phase, where we will extract some data from the actual ledger that the transactions are meant to be imported into. We will implement a generic interface that should allow each ledger language implementation to provide relevant data for training.

The output data here should be in the same format as its input, so that we can optionally skip this phase.

### Rendering<a id="rendering"></a>

An output renderer should be selected by the driver. This is where we convert the extracted data structures to the particular flavor of ledger implementation you’re using. Each of the renderer implementations should be free to import modules from its particular implementation, and we should be careful to constraint these import dependencies to only these modules, to make sure that only a single ledger implementation is required in order for the code to run.

Options for rendering style could be defined here, for each renderer, because each of the languages have particularies.

\[AMaffei\] Also, it should be possible to provide a generic renderer that takes printf-style format strings to output in any desired format.

### Filing<a id="filing"></a>

Importers should be able to look at the textified contents of the files and find the file/statement date. This is useful, because we can rename the file by prepending the date of the statement, and the date at which we download the statement or transaction files is rarely the same date at which it was generated. In the case where we are not able to extract a date from the file, we fall back on the filename’s last modified time.

A target directory should be provided and we should move each file to the account with which it is associated. For example, a file like this:

    ~/Downloads/ofx32755.qbo

should be moved to a directory

    .../Assets/US/RBC/Checking/2013-11-27.ofx32755.qbo

if it is associated by the identification step with an importer for the Assets:US:RBC:Checking account. For this purpose, all the importers should have a required “filing” account associated with them.

As far as I know only Beancount implements this at the moment, but I suspect this convenient mechanism of organizing and preserving your imported files will be found useful by others. Given a list of directories, Beancount automatically finds those files and using the date in the filename, is able to render links to the files as line items in the journal web pages, and serve their contents when the user clicks on the links. Even without this capability, it can be used to maintain a cache of your documents (I maintain mine in a repository which I sync to an external drive for backup).

Implementation Details<a id="implementation-details"></a>
---------------------------------------------------------

Notes about the initial implementation:

-   The implementation of this project will be carried out in Python3. Why Python?

    -   The performance of importing and extracting is largely irrelevant, a dynamic language works well for this type of task

    -   Parsing in a dynamic language works great, there are many available libraries

    -   Python3 is now widely distributed and all desired parsing libraries are commonly available for it at this point

-   The project will be hosted at either [<span class="underline">http://hg.furius.ca/public/ledgerhub/</span>](http://hg.furius.ca/public/ledgerhub/) (or perhaps [<span class="underline">https://bitbucket.org/blais/ledgerhub/</span>](https://bitbucket.org/blais/ledgerhub/) ?)

-   All modules should be tested, including testing with sample input. If you want to add a new module, you should need to provide an anonymized sample file for it. We will have to have an automated test suite, because past experience has shown this type of code to be quite brittle and fragile to new and unexpected inputs. It’s easy to write, but it’s also easy to break.

    -   In order to test binary files that cannot be anonymized, we will provide the ability to test from match-text instead of from original binary statement PDF. Those files are generally not extractable anyhow and are only there for identification and filing (e.g. a PDF statement, we can’t extract any meaningful data out of those except perhaps for the statement date).

-   There should be a quick way to test a particular importer with a particular downloaded file with zero configuration, even if the output account names are a little wonky.

-   There needs to be clean and readable tracing for what the importers are doing, including a debugging/verbose option.

-   We provide a single function to call as the driver for your own import script. Your configuration is a script / your script is the configuration. You call a function at the end. We will also provide a script that imports a filename and fetches an attribute from it, for those who want a more traditional invocation.

-   We should keep types simples, but use the standard datetime types for dates, decimal.Decimal for numbers, and strings for currencies/commodities.

This is obviously based on my current importers code in Beancount. I’m very open to new ideas and suggestions for this project. Collaborations will be most welcome. The more importers we can support, the better.

Importers Interface<a id="importers-interface"></a>
---------------------------------------------------

Each importer should be implemented as a class that derives from this one:

class ImporterBase:  
"Base class/interface for all source importers."  
  
\# A dict of required configuration variables to their docstring.  
\# This declares the list of options required for the importer  
\# to be provided with, and their meaning.  
**REQUIRED\_CONFIG** = {}  
  
def \_\_init\_\_(self, config):  
"""Create an importer.  
Most concrete implementations can just use this without overriding.  
  
Args:  
config: A dict of configuration accounts, that must match the  
REQUIRED\_CONFIG values.  
"""  
\# a dict of Configuration values. This can be accessed publicly.  
assert isinstance(config, dict)  
self.config = config  
  
\# Check that the config has just the required configuration values.  
if not verify\_config(self, config, self.REQUIRED\_CONFIG):  
raise ValueError("Invalid config {}, requires {}".format(  
config, self.REQUIRED\_CONFIG))  
  
def get\_filing\_account(self):  
"""Return the account for moving the input file to.  
  
Returns:  
The name of the account that corresponds to this importer.  
"""  
return self.config\['FILE'\]  
  
def **import\_file**(self, filename):  
"""Attempt to import a file.  
  
Args:  
filename: the name of the file to be imported.  
Returns:  
A list of new, imported entries extracted from the file.  
"""  
raise NotImplementedError  
  
def **import\_date**(self, filename, text\_contents):  
"""Attempt to obtain a date that corresponds to the given file.  
  
Args:  
filename: the name of the file to extract the date from  
text\_contents: an ASCII text version of the file contents,  
whatever format it is originally in.  
Returns:  
A date object, if successful, or None.  
"""  
raise NotImplementedError

For each importer, a detailed explanation of how the original input file on the institution’s website is to be found and downloaded should be provided, to help those find the correct download when adding this importer (some institutions provide a variety of download formats). In addition, a one-line description of the input file support should be provided, so that we can render at runtime a list of the supported file types.

References<a id="references"></a>
---------------------------------

Other projects with the same goal as importing account data into Ledger are listed here.

-   [<span class="underline">Ledger’s “convert” command</span>](http://ledger-cli.org/3.0/doc/ledger3.html#The-convert-command)

-   HLedger with its [<span class="underline">built-in</span>](http://hledger.org/manual#csv-files) [<span class="underline">readers</span>](http://hledger.org/manual#timelog-files)

-   <span class="underline">Reckon</span>

-   [<span class="underline">OFXmate</span>](https://github.com/captin411/ofxmate) (GUI for ledger-autosync)

-   [<span class="underline">CSV2Ledger</span>](https://github.com/jwiegley/CSV2Ledger)

-   [<span class="underline">icsv2ledger</span>](https://github.com/quentinsf/icsv2ledger)

-   [<span class="underline">csv2ledger</span>](http://www.khjk.org/log/2009/oct/csv2ledger.hs) (seems to lack active maintainers)

Update (Nov 2015): This design doc has been implemented and the project is being transitioned back to Beancount. Read the details [<span class="underline">here</span>](https://docs.google.com/document/d/1Bln8Zo11Cvez2rdEgpnM-oBHC1B6uPC18Qm7ulobolM/).
