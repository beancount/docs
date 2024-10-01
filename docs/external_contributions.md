# External Contributions to Beancount<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca) - Updated: June 2024

[<u>http://furius.ca/beancount/doc/contrib</u>](http://furius.ca/beancount/doc/contrib)

    Links to codes written by other people that build on top of or that are related to Beancount and/or Ledgerhub.

## Indexes<a id="indexes"></a>

This document contains only packages that were discussed or have had an announcement sent to the mailing-list. You will be able to find other packages on public indices:

-   PyPI: You can find a lot of other Beancount-related projects at [<u>PyPI</u>](https://pypi.org/search/?q=beancount&o=).

-   GitHub: A [<u>search for "beancount"</u>](https://github.com/search?p=5&q=beancount&ref=opensearch&type=Repositories) as of September 2020 brings up 318 projects.

## Books and Articles<a id="books-and-articles"></a>

[<u>Managing Personal Finances using Python</u>](https://personalfinancespython.com/) (Siddhant Goel): a 2020 book on plain-text accounting, and Beancount.

[<u>The Five Minute Ledger Update</u>](https://reds-rants.netlify.app/personal-finance/the-five-minute-ledger-update/) (RedStreet) A series of articles showing how to automate downloading data from institutions (banks, credit cards, brokerages, etc.) so that ledger updates can be done in under five minutes. [<u>Mailing list thread</u>](https://groups.google.com/g/beancount/c/_NclCTXaExs/m/EFjqkqElAQAJ).

[<u>Tax Loss Harvesting with Beancount</u>](https://reds-rants.netlify.app/personal-finance/tax-loss-harvesting-with-beancount/) (RedStreet): An article about TLH from a US perspective, includes requirements, wash sale subtleties and safe to sell/buy dates, and comparisons to robo-advisors. (Related: [<u>fava\_investor TLH module</u>](https://github.com/redstreet/fava_investor/tree/main/fava_investor/modules/tlh). for fava and plain-beancount command line version).

[<u>Scaled Estimates of Mutual Fund NAVs</u>](https://reds-rants.netlify.app/personal-finance/scaled-estimates-of-mutual-fund-navs/) (RedStreet) : Problem: Mutual fund NAVs (at least in the US) are updated exactly once per day, at the end of the day. When needing to make financial decisions when the trading window is still open (eg: when tax loss harvesting), and the end-of-day NAV is not yet available, it is sometimes useful to make a trivial estimate of that NAV, especially on days when there are huge changes in the market.

[<u>A Shortcut to Scrape Trade History from Fidelity</u>](https://noisysignal.com/trade_hist_shortcut/) (David Avraamides) I wrote up a description of how I use a Shortcut to scrape trade history from Fidelity’s website, run it through a Python script to convert to Beancount’s ledger format, and then save it in the clipboard so I can paste it into a ledger file.

[<u>Lazy Beancount</u>](https://lazy-beancount.xyz/) (Vasily M) / [<u>Evernight/lazy-beancount</u>](https://github.com/Evernight/lazy-beancount) : Opinionated guide on how to start (and continue) tracking personal finances using the open-source Beancount accounting system. It comes together with some code. The primary goal of this guide is to provide you a way to start managing your own finances using plain-text accounting gradually and incrementally. Also with various useful tools already included and set up.

[<u>The Zen of Balance — https://academy.beanhub.io/</u>](https://academy.beanhub.io/) (Fang-Pen Lin) : An explanation of double-entry accounting using visualizations and diagrams.

[<u>Multiperiod hledger-Style Reports in beancount: Pivoting a Table | Altynbek Isabekov</u>](https://www.isabekov.pro/multiperiod-hledger-style-reports-in-beancount-pivoting-a-table/) : An article showing how to produce pivot table summaries of account balances, e.g. by year, with [<u>associated code (github)</u>](https://github.com/isabekov/beancount-multiperiod-reports).

## Plugins<a id="plugins"></a>

[<u>split\_transactions</u>](https://www.google.com/url?q=https%3A%2F%2Fgist.github.com%2Fkljohann%2Faebac3f0146680fd9aa5&sa=D&sntz=1&usg=AFQjCNGn2AkL35onTeXgOQzLzkjVpvLcpg): Johann Klähn [<u>wrote a plugin</u>](https://groups.google.com/d/msg/beancount/z9sPboW4U3c/1qIIzro4zFoJ) that can split a single transaction into many against a limbo account, as would be done for depreciation.

[<u>zerosum</u>](https://github.com/redstreet/beancount_reds_plugins): Red S [<u>wrote a plugin</u>](https://groups.google.com/d/msg/beancount/MU6KozsmqGQ/sehD3dqZslEJ) to match up transactions that when taken together should sum up to zero and move them to a separate account.

[<u>effective\_dates</u>](https://github.com/redstreet/beancount_reds_plugins): Red S wrote a plugin to book different legs of a transaction to different dates

[<u>beancount-plugins</u>](https://github.com/davidastephens/beancount-plugins): Dave Stephens created a repository to share various of his plugins related to depreciation.

[<u>beancount-plugins-zack</u>](https://github.com/zacchiro/beancount-plugins-zack): Stefano Zacchiroli created this repository to share his plugins. Contains sorting of directives and more.

<u>b[eancount-oneliner](https://github.com/Akuukis/beancount-oneliner)</u>: Akuukis created a plugin to write an entry in one line ([<u>PyPi</u>](https://pypi.python.org/pypi/beancount-oneliner/1.0.0)).

[<u>beancount-interpolate</u>](https://github.com/Akuukis/beancount-interpolate): Akuukis created plugins for Beancount to interpolate transactions (recur, split, depr, spread) ([<u>PyPi</u>](https://pypi.python.org/pypi/beancount-interpolate)).

[<u>metadata-spray</u>](https://github.com/seltzered/beancount-plugins-metadata-spray): Add metadata across entries by regex expression rather than having explicit entries (by Vivek Gani).

[<u>Akuukis/beancount\_share</u>](https://github.com/Akuukis/beancount_share): A beancount plugin to share expenses among multiple partners within one ledger. This plugin is very powerful and most probably can deal with all of your sharing needs.

[<u>w1ndy/beancount\_balexpr</u>](https://github.com/w1ndy/beancount_balexpr) (Di Weng): A plugin that provides "balance expressions" to be run against the Beancount entries, as a Custom directive. See [<u>this thread</u>](https://groups.google.com/d/msgid/beancount/cdcf2cc7-8061-4f69-ae6a-c82564463652n%40googlegroups.com?utm_medium=email&utm_source=footer).

[<u>autobean.narration</u>](https://git.io/autobean.narration) (Archimedes Smith): Allows to annotate each posting in a concise way by populating per-posting narration metadata from inline comments.

[<u>autobean.sorted</u>](https://github.com/SEIAROTg/autobean/): Checks that transactions are in non-descending order in each file. Helps identifying misplaced or misdated directives, by warning on those directives not following a non-descending order by date in the file.

[<u>hoostus/beancount-asset-transfer-plugin</u>](https://github.com/hoostus/beancount-asset-transfer-plugin): A plugin to automatically generate in-kind transfers between two beancount accounts, while preserving the cost basis and acquisition date.

[<u>PhracturedBlue/fava-portfolio-summary</u>](https://github.com/PhracturedBlue/fava-portfolio-summary) (Phractured Blue): Fava Plugin to show portfolio summaries with rate of return.

[<u>rename\_accounts</u>](https://github.com/redstreet/beancount_reds_plugins): Plugin from Red S to rename accounts. E.g.: rename “Expenses:Taxes” to “Income:Taxes” is helpful for expense analysis. [<u>More here</u>](https://github.com/redstreet/beancount_reds_plugins/tree/main/beancount_reds_plugins/rename_accounts#readme).

[<u>Long\_short capital gains classifier</u>](https://github.com/redstreet/beancount_reds_plugins/tree/master/beancount_reds_plugins/capital_gains_classifier): Plugin from Red S to classify capital gains into long and short based on duration the assets were held, and into gains and losses based on value.

[<u>Autoclose\_tree</u>](https://github.com/redstreet/beancount_reds_plugins/tree/main/beancount_reds_plugins/autoclose_tree): Automatically closes all of an account's descendants when an account is closed.

[<u>Evernight/beancount-valuation</u>](https://github.com/Evernight/beancount-valuation) (Vasily M) : A Beancount plugin to track total value of the opaque fund. You can use it instead of the balance operation to assert total value of the account. If the value of the account is currently different, it will instead alter price of the underlying synthetical commodity created by the plugin used for technical purposes.

## Tools<a id="tools"></a>

[<u>alfred-beancount</u>](https://github.com/blaulan/alfred-beancount) (Yue Wu): An add-on to the “Alfred” macOS tool to quickly enter transactions in one’s Beancount file. Supports full account names and payees match.

[<u>bean-add</u>](https://github.com/simon-v/bean-add) (Simon Volpert): A Beancount transaction entry assistant.

[<u>hoostus/fincen\_114</u>](https://github.com/hoostus/fincen_114) (Justus Pendleton): An FBAR / FinCEN 114 report generator.

[<u>ghislainbourgeois/beancount\_portfolio\_allocation</u>](https://github.com/ghislainbourgeois/beancount_portfolio_allocation) ([<u>Ghislain Bourgeois</u>](https://groups.google.com/d/msgid/beancount/b36d9b67-8496-4021-98ea-0470e5f09e4b%40googlegroups.com?utm_medium=email&utm_source=footer)): A quick way to figure out the asset allocations in different portfolios.

[<u>hoostus/portfolio-returns</u>](https://github.com/hoostus/portfolio-returns) (Justus Pendleton): portfolio returns calculator

[<u>costflow/syntax</u>](https://github.com/costflow/syntax) (Leplay Li): A product that allows users to keep plain text accounting from their favorite messaging apps. A syntax for converting one-line message to beancount/\*ledger format.

[<u>process control chart</u>](https://github.com/hoostus/beancount-control-chart) (Justus Pendleton): Spending relative to portfolio size. [<u>Thread.</u>](https://groups.google.com/d/msgid/beancount/0cd47f9a-37d6-444e-8516-25e247a9e0cd%40googlegroups.com?utm_medium=email&utm_source=footer)

[<u>Pinto</u>](https://pypi.org/project/pinto/) (Sean Leavey): Supercharged command line interface for Beancount. Supports automatic insertions of transactions in ledger file.

[<u>PhracturedBlue/fava-encrypt</u>](https://github.com/PhracturedBlue/fava-encrypt) : A docker-base solution for keeping Fava online while keeping beancount data encrypted at rest. See [<u>this thread</u>](https://groups.google.com/d/msgid/beancount/ece6f424-a86b-4e6d-8ecc-4e05c8e74373n%40googlegroups.com?utm_medium=email&utm_source=footer) for context.

[<u>kubauk/beancount-import-gmail</u>](https://github.com/kubauk/beancount-import-gmail) : beancount-import-gmail uses the gmail API and OAuth to log into your mailbox and download order details which are then used to augment your transactions for easier classification.

[<u>sulemankm/budget\_report</u>](https://github.com/sulemankm/budget_report) : A very simple command-line budget tracking tool for beancount ledger files.

[<u>dyumnin/dyu\_accounting</u>](https://github.com/dyumnin/dyu_accounting) : Accounting setup to automate generation of various financial statements for Compliance with Indian Govt.

[<u>Gains Minimizer</u>](https://github.com/redstreet/fava_investor/tree/main/fava_investor/modules/minimizegains) (RedStreet): Automatically determine lots to sell to minimize capital gains taxes. [<u>Live example.</u>](http://favainvestor.pythonanywhere.com/example-beancount-file/extension/Investor/?module=minimizegains)

[<u>beanahead</u>](https://github.com/maread99/beanahead) (Marcus Read): Adds the ability to include future transactions (automatically generates regular transactions, provides for ad hoc expected transactions, expected transactions are reconciled against imported transactions; all functionality accessible via cli).

[<u>autobean-format</u>](https://github.com/SEIAROTg/autobean-format) (Archimedes Smith): Yet another formatter for beancount,, powered by earlier project autobean-refactor, a library for parsing and programmatically manipulating beancount files. based on a proper parser, allowing it to format every corner of your ledger, including arithmetic expressions.

[<u>akirak/flymake-bean-check</u>](https://github.com/akirak/flymake-bean-check) (Akira Komamura): flymake support for Emacs.

[<u>bean-download</u>](https://reds-rants.netlify.app/personal-finance/direct-downloads/) (Red Street): A downloader that ships with beancount-reds-importers that you can configure to run arbitrary commands to download your account statements. It now has a new feature: the needs-update subcommand.

[<u>gerdemb/beanpost</u>](https://github.com/gerdemb/beanpost) (Ben Gerdemann): Beanpost consists of a PostgreSQL schema and import/export commands that let you transfer data between a beancount file and a PostgreSQL database. Much of Beancount's functionality is implemented using custom PostgreSQL functions, allowing for complex queries and data manipulation. This setup provides a flexible backend that can integrate with other tools like web apps or reporting systems

[<u>LaunchPlatform/beanhub-cli</u>](https://github.com/LaunchPlatform/beanhub-cli) (Fang-Pen Lin): Command line tools for BeanHub or Beancount users.

[<u>zacchiro/beangrep</u>](https://github.com/zacchiro/beangrep) : Beangrep is a grep-like filter for the Beancount plain text accounting system.

## Alternative Parsers<a id="alternative-parsers"></a>

### Bison<a id="bison"></a>

The Beancount v2 parser uses GNU flex + GNU bison (for maximum portability).

The Beancount v3 parser uses [<u>RE/flex</u>](https://www.genivia.com/doc/reflex/html/) + GNU bison (for Unicode and C++).

### Using Antlr<a id="using-antlr"></a>

[<u>jord1e/jbeancount</u>](https://github.com/jord1e/jbeancount) (Jordie Biemold) / using Antlr: An alternative parser for Beancount input syntax in Java (using the Antlr4 parser generator). This provides access to parsed Beancount data - without the effect of plugins - from JVM languages. See [<u>this post</u>](https://groups.google.com/d/msgid/beancount/72ee8adb-a376-4e30-b6d4-ea8749f5f666n%40googlegroups.com?utm_medium=email&utm_source=footer) for details.

### Using Tree-sitter<a id="using-tree-sitter"></a>

[<u>polarmutex/tree-sitter-beancount</u>](https://github.com/polarmutex/tree-sitter-beancount) (Bryan Ryall): A tree-sitter parser for the Beancount syntax.

[<u>https://github.com/dnicolodi/tree-sitter-beancount</u>](https://github.com/dnicolodi/tree-sitter-beancount) (Daniele Nicolodi): Another tree-sitter based parser for the Beancount syntax.

### In Rust<a id="in-rust"></a>

[<u>jcornaz/beancount-parser</u>](https://github.com/jcornaz/beancount-parser) (Jonathan Cornaz): A beancount file parser library for Rust. Uses nom.

[<u>beancount\_parser\_lima</u>](https://docs.rs/beancount-parser-lima/latest/beancount_parser_lima/) (Simon Guest): A zero-copy parser for Beancount in Rust. It is intended to be a complete implementation of the Beancount file format, except for those parts which are deprecated and other features as documented here (in a list which may not be comprehensive). Uses [<u>Logos</u>](https://docs.rs/logos/latest/logos/), [<u>Chumsky</u>](https://docs.rs/chumsky/latest/chumsky/), and [<u>Ariadne</u>](https://docs.rs/ariadne/latest/ariadne/).

### Emacs Lisp<a id="emacs-lisp"></a>

[<u>trs-80/beancount-txn-elisp/</u>](https://sr.ht/~trs-80/beancount-txn-elisp/) : beancount-txn-elisp: A library to read/parse and write/insert individual Beancount transactions, implemented in Emacs Lisp.

## Importers<a id="importers"></a>

[<u>reds importers</u>](https://github.com/redstreet/beancount_reds_importers): Simple importers and tools for [<u>several</u>](https://github.com/redstreet/beancount_reds_importers/tree/main/beancount_reds_importers) US based institutions, and various file types. Emphasizes ease of writing your own importers by providing well maintained common libraries for banks, credit cards, and investment houses, and for various file types, which minimizes the institution specific code you need to write. This is a reference implementation of the principles expressed in **[<u>The Five Minute Ledger Update</u>](https://reds-rants.netlify.app/personal-finance/the-five-minute-ledger-update/).** Contributions welcome. By RedStreet

[<u>plaid2text</u>](https://github.com/madhat2r/plaid2text): An importer from [<u>Plaid</u>](http://www.plaid.com/) which stores the transactions to a Mongo DB and is able to render it to Beancount syntax. By Micah Duke.

[<u>jbms/beancount-import</u>](https://github.com/jbms/beancount-import): A tool for semi-automatically importing transactions from external data sources, with support for merging and reconciling imported transactions with each other and with existing transactions in the beancount journal. The UI is web based. ([<u>Announcement</u>](https://github.com/jbms/beancount-import), [<u>link to previous version</u>](https://groups.google.com/d/msg/beancount/YN3xL09QFsQ/qhL8U6JDCgAJ)). By Jeremy Maitin-Shepard.

[<u>awesome-beancount</u>](https://github.com/wzyboy/awesome-beancount): A collection of importers for Chinese banks + tips and tricks. By [<u>Zhuoyun Wei</u>](https://github.com/wzyboy).

[<u>beansoup</u>](https://github.com/fxtlabs/beansoup): Filippo Tampieri is sharing some of his Beancount importers and auto-completer in this project.

[<u>montaropdf/beancount-importers</u>](https://github.com/montaropdf/beancount-importers/): An importer to extract overtime and vacation from a timesheet format for invoicing customers.

[<u>siddhantgoel/beancount-dkb</u>](https://github.com/siddhantgoel/beancount-dkb) (Siddhant Goel): importer for DKB CSV files.

[<u>prabusw/beancount-importer-zerodha</u>](https://github.com/prabusw/beancount-importer-zerodha): Importer for the Indian broker Zerodha.

[<u>swapi/beancount-utils</u>](https://github.com/swapi/beancount-utils) : Another importer for Zerodha.

[<u>Dr-Nuke/drnuke-bean</u>](https://github.com/Dr-Nuke/drnuke-bean) (Dr Nuke): An importer for IBKR, based on the flex query (API-like) and one for Swiss PostFinance.

[<u>Beanborg</u>](https://github.com/luciano-fiandesio/beanborg) (Luciano Fiandesio): Beanborg automatically imports financial transactions from external CSV files into the Beancount bookkeeping system.

[<u>szabootibor/beancount-degiro</u>](https://gitlab.com/szabootibor/beancount-degiro) ([<u>PyPI</u>](https://pypi.org/project/beancount-degiro)): Importer for the trading accounts of the Dutch broker Degiro.

[<u>siddhantgoel/beancount-ing-diba</u>](https://github.com/siddhantgoel/beancount-ing-diba) ([<u>PyPI</u>](https://pypi.org/project/beancount-ing-diba/)): ING account importer (NL).

[<u>PaulsTek/csv2bean</u>](https://github.com/PaulsTek/csv2bean) : Asimple application to preprocess csv files using google sheets in Go.

[<u>ericaltendorf/magicbeans</u>](https://github.com/ericaltendorf/magicbeans) (Eric Altendorf): Beancount importers for crypto data. Detailed lot tracking and capital gains/losses reporting for crypto assets. " I wrote it because I was not satisfied with the accuracy or transparency of existing commercial services for crypto tax reporting."

[<u>OSadovy/uabean</u>](https://github.com/OSadovy/uabean/) (Oleksii Sadovyi): A set of Beancount importers and scripts for popular Ukrainian banks and more.

[<u>fdavies93/seneca</u>](https://github.com/fdavies93/seneca) (Frank Davies): Importer for Wise. Multi-currency transfers.

[<u>LaunchPlatform/beanhub-import</u>](https://github.com/LaunchPlatform/beanhub-import) : New beancount importer with a UI.

[<u>rlan/beancount-multitool</u>](https://github.com/rlan/beancount-multitool) (Rick Lan): Beancount Multitool is a command-line-interface (CLI) tool that converts financial data from financial institutions to Beancount files (supported: JA Bank ＪＡネットバンク, Rakuten Card 楽天カード, Rakuten Bank 楽天銀行, SBI Shinsei Bank 新生銀行). Associated post: [<u>https://www.linkedin.com/feed/update/urn:li:activity:7198125470662500352/</u>](https://www.linkedin.com/feed/update/urn:li:activity:7198125470662500352/)

[<u>LaunchPlatform/beanhub-import</u>](https://github.com/LaunchPlatform/beanhub-import) (Fang-Pen Lin): Beanhub-import is a simple, declarative, smart, and easy-to-use library for importing extracted transactions from beanhub-extract. It generates Beancount transactions based on predefined rules.

## Converters<a id="converters"></a>

[<u>plaid2text</u>](https://github.com/madhat2r/plaid2text): Python Scripts to export Plaid transactions and transform them into Ledger or Beancount syntax formatted files.

[<u>gnucash-to-beancount</u>](https://github.com/henriquebastos/gnucash-to-beancount/): A script from Henrique Bastos to convert a GNUcash SQLite database into an equivalent Beancount input file.

[<u>debanjum/gnucash-to-beancount</u>](https://github.com/debanjum/gnucash-to-beancount): A fork of the above.

[<u>andrewStein/gnucash-to-beancount</u>](https://github.com/AndrewStein/gnucash-to-beancount) : A further fork from the above two, which fixes a lot of issues (see [<u>this thread</u>](https://groups.google.com/d/msg/beancount/MaaASKR1SSI/GX5I8lOkBgAJ)).

[<u>hoostus/beancount-ynab</u>](https://github.com/hoostus/beancount-ynab) : A converter from YNAB to Beancount.

[<u>hoostus/beancount-ynab5</u>](https://github.com/hoostus/beancount-ynab5) : Same convert for YNAB from the same author, but for the more recent version 5.

[<u>ledger2beancount</u>](https://github.com/zacchiro/ledger2beancount/): A script to convert ledger files to beancount. It was developed by Stefano Zacchiroli and Martin Michlmayr.

[<u>smart\_importer</u>](https://github.com/johannesjh/smart_importer): A smart importer for beancount and fava, with intelligent suggestions for account names. By Johannes Harms.

[<u>beancount-export-patreon.js</u>](https://gist.github.com/riking/0f0dab2b7761d2f6895c5d58c0b62a66): JavaScript that will export your Patreon transactions so you can see details of exactly who you've been giving money to. By kanepyork@gmail.

[<u>alensiljak/pta-converters</u>](https://gitlab.com/alensiljak/pta-converters) (Alen Šiljak): GnuCash -&gt; Beancount converter (2019).

[<u>grostim/Beancount-myTools</u>](https://github.com/grostim/Beancount-myTools) (Timothee Gros): Personal importer tools of the author for French banks.

## Downloaders<a id="downloaders"></a>

[<u>bean-download</u>](https://github.com/redstreet/beancount_reds_importers) (RedStreet): bean-download is a tool to conveniently download your transactions from supporting institutions. You configure it with a list of your institutions and arbitrary commands to download them, typically via [<u>ofxget</u>](https://ofxtools.readthedocs.io/en/latest/). It downloads all of them in parallel, names them appropriately and puts them in the directory of your choice, from which you can then import. The tool is installed as a part of [<u>beancount-reds-importers</u>](https://github.com/redstreet/beancount_reds_importers). See [<u>accompanying article</u>](https://reds-rants.netlify.app/personal-finance/direct-downloads/).

[<u>ofx-summarize</u>](https://github.com/redstreet/beancount_reds_importers) (RedStreet): When building importers, it helps to be able to peek into a .ofx or a .qfx file that you are trying to import. The ofx-summarize command does just that. It ships with [<u>beancount-reds-importers</u>](https://github.com/redstreet/beancount_reds_importers), and should be available by simply invoking the command. Running the command on a file shows you a few transactions in the file. What is very useful is to be able to explore your .ofx file via the python debugger or interpreter.

## Price Sources<a id="price-sources"></a>

[<u>hoostus/beancount-price-sources</u>](https://github.com/hoostus/beancount-price-sources) : A Morningstar price fetcher which aggregates multiple exchanges, including non-US ones.

[<u>andyjscott/beancount-financequote</u>](https://github.com/andyjscott/beancount-financequote) : Finance::Quote support for bean-price.

[<u>aamerabbas/beancount-coinmarketcap</u>](https://github.com/aamerabbas/beancount-coinmarketcap): Price fetcher for coinmarketcap ([<u>see post</u>](https://medium.com/@danielcimring/downloading-historical-data-from-coinmarketcap-41a2b0111baf)).

[<u>grostim/Beancount-myTools/.../iexcloud.py</u>](https://github.com/grostim/Beancount-myTools/blob/master/price/iexcloud.py) : Price fetcher for iexcloud by Timothee Gros.

[<u>xuhcc/beancount-cryptoassets</u>](https://github.com/xuhcc/beancount-cryptoassets) (Kirill Goncharov): Price sources for cryptocurrencies.

[<u>xuhcc/beancount-ethereum-importer</u>](https://github.com/xuhcc/beancount-ethereum-importer) (Kirill Goncharov): Ethereum transaction importer for Beancount. Includes a script that downloads transactions from Etherscan and an importer for downloaded transactions.

[<u>xuhcc/beancount-exchangerates</u>](https://github.com/xuhcc/beancount-exchangerates) (Kirill Goncharov): Price source for [<u>http://exchangeratesapi.io</u>](http://exchangeratesapi.io).

[<u>tarioch/beancounttools</u>](https://github.com/tarioch/beancounttools) (Patrick Ruckstuhl): Price sources and importers.

[<u>https://gitlab.com/chrisberkhout/pricehist</u>](https://gitlab.com/chrisberkhout/pricehist) (Chris Berkhout): A command-line tool that can fetch daily historical prices from multiple sources and output them in several formats. Supports some sources for CoinDesk, European Central Bank, Alpha Vantage, CoinMarketCap. The user can request a specific price type such as high, low, open, close or adjusted close. It can also be used through bean-price.

## Development<a id="development"></a>

[<u>Py3k type annotations</u>](https://github.com/yegle/beancount-type-stubs): Yuchen Ying is implementing python3 type annotations for Beancount.

[<u>bryall/tree-sitter-beancount</u>](https://github.com/bryall/tree-sitter-beancount) (Bryan Ryall): A tree-sitter parser for the beancount syntax.

[<u>jmgilman/beancount-stubs</u>](https://github.com/jmgilman/beancount-stubs): Typing .pyi stubs for some of the Beancount source.

## Documentation<a id="documentation"></a>

[<u>Beancount Documentation</u>](https://beancount.github.io/docs/) ([<u>Kirill Goncharov</u>](http://github.com/xuhcc)): Official conversion of the Beancount documentation from Google Docs source to Markdown and HTML. This includes most of the Google Docs documents and is maintained in a Beancount org repo [<u>here</u>](http://github.com/beancount/docs) by Kirill Goncharov.

[<u>Beancount Source Code Documentation</u>](http://aumayr.github.io/beancount-docs-static/) ([<u>Dominik Aumayr</u>](http://github.com/aumayr)): A Sphinx-generated source code documentation of the Beancount codebase. The code to produce this is [<u>located here</u>](https://github.com/aumayr/beancount-docs).

[<u>SQL queries for Beancount</u>](http://aumayr.github.io/beancount-sql-queries/) (Dominik Aumayr): Example SQL queries.

[<u>Beancount —— 命令行复式簿记</u>](https://wzyboy.im/post/1063.html) (Zhuoyun Wei): A tutorial (blog post) in Chinese on how to use Beancount.

[<u>Managing my personal finances with Beancount</u>](https://alexjj.com/blog/2016/2/managing-my-personal-finances-with-beancount/) (Alex Johnstone)

[<u>Counting beans—and more—with Beancount</u>](https://lwn.net/SubscriberLink/751874/a38128abb72e45c5/) (LWN)

## Interfaces / Web<a id="interfaces-web"></a>

[<u>fava: A web interface for Beancount</u>](https://github.com/aumayr/fava) (Dominik Aumayr, Jakob Schnitzer): Beancount comes with its own simple web front-end (“bean-web”) intended merely as a thin shell to invoke and display HTML versions of its reports. “Fava” is an alternative web application front-end with more & different features, intended initially as a playground and proof-of-concept to explore a newer, better design for presenting the contents of a Beancount file.

[<u>Fava Classy Portfolio</u>](https://github.com/seltzered/fava-classy-portfolio) (Vivek Gani): Classy Portfolio is an Extension for Fava, a web interface for the Beancount plaintext accounting software. The extension displays a list of different portfolios (e.g. 'taxable' vs. 'retirement'), with breakdowns using 'asset-class' and 'asset-subclass' metadata labels on commodities.

[<u>Fava Investor</u>](https://github.com/redstreet/fava_investor) project (RedStreet): Fava\_investor aims to be a comprehensive set of reports, analyses, and tools for investments, for Beancount and Fava. It is a collection of modules, with each module offering a Fava plugin, a Beancount library, and a Beancount based CLI (command line interface). Current modules include: Visual, tree structured asset allocation by class, asset allocation by account, tax loss harvester, cash drag analysis.

[<u>Fava Miler</u>](https://github.com/redstreet/fava_miler) (RedStreet): Airline miles and rewards points: expiration and value reporting.

[<u>Fava Envelope</u>](https://github.com/bryall/fava-envelope) (Brian Ryall): A beancount fava extension to add an envelope budgeting capability to fava and beancount. It is developed as a Fava plugin and CLI.

[<u>scauligi/refried</u>](https://github.com/scauligi/refried) (Sunjay Cauligi): An envelope budgeting plugin for Fava, inspired by YNAB: all expense accounts become individual budgeting categories, budgeting is carried out using transactions to these accounts, and the plugin automaticallyapplies a tag to all rebudget transactions so they can easily be filtered out. Provides budget and account views like YNAB.

[<u>BeanHub.io</u>](https://beanhub.io/): A web front-end for Beancount content. "*Since I started using Beancount, I have dreamed of making it fully automatic. For a few years now, I've been building tools for that goal. Connecting to the bank and fetching data directly from there is one of the goals I want to achieve. I built this feature and have been testing it for a while for my accounting book. Now my Beancount books are 80% fully automatic. I can open my repository, and the transactions from the bank will automatically appear as a new commit like this without me lifting a finger.*

*The whole import system is based on our open-source beanhub-import and beanhub-extract. The only proprietary part in the import flow is the Plaid integration. So, suppose you don't trust me and still want to import transactions automatically. As long as you connect to Plaid and write CSV files based on the transactions you fetched from Plaid, you should be able to have the same automatic transaction importing system without using the BeanHub service.*"

Blog posts:

> [<u>https://beanhub.io/blog/2024/06/24/introduction-of-beanhub-connect/</u>](https://beanhub.io/blog/2024/06/24/introduction-of-beanhub-connect/)
>
> [<u>https://beanhub.io/blog/2024/04/23/how-beanhub-works-part1-sandboxing/</u>](https://beanhub.io/blog/2024/04/23/how-beanhub-works-part1-sandboxing/)
>
> [<u>https://beanhub.io/blog/2024/06/26/how-beanhub-works-part2-layer-based-git-repos/</u>](https://beanhub.io/blog/2024/06/26/how-beanhub-works-part2-layer-based-git-repos/)

[<u>jmgilman/bdantic</u>](https://github.com/jmgilman/bdantic): A package for extending beancount with [<u>pydantic</u>](https://pydantic-docs.helpmanual.io/). With this package you can convert your ledger to JSON, and more.

[<u>autobean/refactor</u>](https://github.com/SEIAROTg/autobean/tree/master/autobean/refactor) (Archimedes Smith): Tooling to programmatically edit one's ledger, including formatting, sorting, refactoring, rearranging accounts, optimizing via plugins, migration from v2, inserting transactions in a ledger on import, and more.

[<u>seltzered/beancolage</u>](https://github.com/seltzered/beancolage) (Vivek Gani): An Eclipse Theia (vendor-agnostic vscode) app that tries to bundle existing beancount-based packages such as vscode-beancount and Fava.

[<u>aaronstacy.com/personal-finances-dashboard</u>](http://aaronstacy.com/personal-finances-dashboard/) : HTML + D3.js visualization dashboard for Beancount data.

[<u>https://github.com/aleyoscar/beancount-pulsar</u>](https://github.com/aleyoscar/beancount-pulsar) : A Pulsar package for Beancount - Plain Text Accounting, with syntax highlighting, toggling comments, snippets for some directives and automatic indentation. Pulsar package: [<u>https://web.pulsar-edit.dev/packages/beancount-pulsar</u>](https://web.pulsar-edit.dev/packages/beancount-pulsar)

## Mobile/Phone Data Entry<a id="mobilephone-data-entry"></a>

[<u>Beancount Mobile</u>](https://play.google.com/store/apps/details?id=link.beancount.mobile) App (Kirill Goncharov): A mobile data entry app for Beancount. (Currently only Android is supported.) Repo: [<u>https://github.com/xuhcc/beancount-mobile</u>](https://github.com/xuhcc/beancount-mobile) ([<u>Announcement</u>](https://groups.google.com/d/msgid/beancount/014e0879-70e0-4cac-b884-82d8004e1b43%40googlegroups.com?utm_medium=email&utm_source=footer)).

[<u>http://costflow.io</u>](http://costflow.io/): Plain Text Accounting in WeChat. "*Send a message to our bot in Telegram, Facebook Messenger, Whatsapp, LINE, WeChat, etc. Costflow will transform your message into Beancount / Ledger / hledger format transaction magically. Append the transaction to the file in your Dropbox / Google Drive. With the help of their apps, the file will be synced to your computer.*"
