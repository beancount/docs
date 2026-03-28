# Beangulp<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca), Jan 2021

    Importing data for Beancount has been supported originally by the LedgerHub project along with a library of importers, then reintegrated as a pure framework library (with some examples) in the Beancount repo as beancount.ingest, and now we're splitting up that repository again and will factor out the importing framework to another repo for easier maintenance and evolution. This document lays out some of the changes desired in this new version.

## New Repo<a id="new-repo"></a>

The new repository will be located at

> [<u>http://github.com/beancount/beangulp</u>](http://github.com/beancount/beangulp)

Beangulp will target compatibility with the latest beancount release from the v3 branch only.

Beancount v3 is expected to evolve rapidly at the beginning, thus, to make the life of early adopters less painful, careful use of version number increments and versioned dependencies should be employed. Ideally, Beangulp should depend on the current minor version of Beancount only, for example, if Beancount 3.0.0 is released, Beangulp should declare

    install_requires: beancount >3.0, <3.1

See [<u>setuptools doc</u>](https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html#declaring-required-dependency) and [<u>PEP-440</u>](https://www.python.org/dev/peps/pep-0440/#version-specifiers).

## Status<a id="status"></a>

As of Jan 2022, most of this proposal is complete and implemented. (Thanks to Daniele Nicolodi for doing most of the work.)

## Changes<a id="changes"></a>

### Library Only<a id="library-only"></a>

The current implementation allows one to use

1.  the bean-identify, bean-extract and bean-file tools on a "config file" which is evaluated Python, or

2.  create a script and call a single endpoint that will implement the subcommands.

In order to make this work, a really convoluted trampoline is used to bounce the evaluation to the same code. I'll admit it trumps even me who wrote it whenever I have to go in there and edit that code. It also makes it inconvenient to let users add custom before/after customizations to their import process.

The next version will support only (2). The bean-identify, bean-extract, bean-file programs will all be removed. The user will be expected to write their own script.

### One File<a id="one-file"></a>

Right now, each importer consists of two files: the implementation file and an associated test file, e.g.

    soandso_bank.py
    soandso_bank_test.py

The test file is small and usually calls out to a library function to find model files and expected outputs. Since there's hardly any real test code, we'd like to be able to have a single Python file that contains its test invocation.

A new endpoint will be added to define the tests in the importer implementation.

### Self-Running<a id="self-running"></a>

Moreover, that new function should also be the same one as that which is used to put together the configuration script. In other words, an importer's main() function should be equivalent to an importer's invocation with a single configured importer, one that is configured with the configuration used for testing.

This will allow users to just "run the importer" on a specific set of files without having to define a configuration, by using the test configuration, like this:

    soandso_bank.py extract ~/Downloads/transactions.csv

Having this option makes it super convenient for people to share the one file and test it out immediately, without having to create a configuration nor a main program.

I don’t think there is an easy clean way to implement this other than having something like

`if __name__ == ‘__main__’:`

        	    main = Ingest([SoAndSoBankImporter()])
        	    main()

in the importer definition file. This should work right now without changes. Although, it is often the case now that importers require a bit of configuration to work (I am not sure, I don’t use any of the importers distributed with Beancount or widely used).

### **Test** S**ubcommand & Generate**<a id="test-subcommand-generate"></a>

Since the importers are runnable and define their test cases for pytest to run over, we should also add a subcommand "test" to complete "identify", "extract" and "file". That venue is also a great place to replace the --generate option which required ugly injection of the pytestconfig, and instead, implement it ourselves and add a second subcommand: "genexpect" to generate the expected file for testing.

The interface becomes:

    soandso_bank.py identify ~/Downloads/
    soandso_bank.py extract ~/Downloads/
    soandso_bank.py file ~/Downloads/ ~/documents
    soandso_bank.py test ~/documents/testdocs
    soandso_bank.py generate ~/Downloads/transactions.csv

This way we can remove the pytestconfig dep injection and also simplify the logic of unit tests, which had to handle both the check vs. generate scenarios. This should result in simpler code.

### One Expected File<a id="one-expected-file"></a>

Expected outputs from an importer are stored in multiple files with suffixes .extract, .file\_name, .file\_date, etc. If we had all the output in one file, the "genexpect" subcommand could generate everything to stdout. This is convenient.

> myimporter.py
>
> myimporter.beancount

Leverage the Beancount syntax to store the expected values for "file\_name()", "file\_date()" and other outputs. Store those in Event or Custom directives and have the testing code assert on them. The new contents of a test directory should be simple pairs of (a) original downloaded file and (b) expected output, containing the transactions but also all the other method outputs.

### Duplicates Identification<a id="duplicates-identification"></a>

This has never really worked properly. I think if this was implemented separately based on each importer — in other words, letting each importer define how to identify duplicates, e.g., if a unique transaction ID can be assumed having been inserted as a link to disambiguate — we could do this a lot cleaner.

It would be ideal if each importer could specify duplicate id detection, in the importer. It could call on a more general but less reliable method, and that code should live in Beangulp.

### CSV Utils<a id="csv-utils"></a>

I have a lot of really convenient utilities for slicing and dicing CSV files from ugly CSV downloads. CSV downloads often are used to house multiple tables and types of data, and a higher-level of processing is often needed on top of these files.

I have code like this spread all over. This deserves a nice library. What's more, I have a nice table processing library under the Baskets project, which hasn't been given the proper quality treatment yet.

Clean up my little table library and merge it with all the CSV utils. Put this in beangulp, or even contemplate making this its own project, including a CSV importer. "CSV world."

*Not sure this matters as much after discovering petl. We could depend on petl.*

### Caching<a id="caching"></a>

When running conversion jobs on large files, it would be nice to have a cache and avoid running those more than once. The (small) converted data could be cached and loaded back up in order to avoid running the expensive conversion more than once. One difficulty is that the conversions required to be run depend on the importers configuration, and each importer is unaware of the other ones.

All the command-line arguments and at least the head of the file contents should be hashed in. This library could be pretty independent from Beancount.

### API Changes<a id="api-changes"></a>

-   "file\_date()" is not clear; "get\_filing\_date()" would be.

-   The extra argument on extract() is irregular compared to all the other methods. Find a better way?

-   I'm not 100% sure I like my little memoizing file wrapper ("cache") with cache. Replace it with a disk-only one.

### Automatic Insertion<a id="automatic-insertion"></a>

A really convenient and easily built feature that the new code should have is the automatic insertions of the extracted output to an existing ledger, before the point of a special string token in the file. Make this part of the library, as an alternative for storing the output of the importer, e.g.

`$ ./myimport.py extract | bean-insert ledger.beancount Amex`

This could also be a flag to "extract"

`$ ./myimport.py extract -f ledger.beancount -F Amex`
