External Contributions to Beancount<a id="title"></a>
=====================================================

[<span class="underline">Martin Blais</span>](mailto:blais@furius.ca) - Updated: April 2016

[<span class="underline">http://furius.ca/beancount/doc/contrib</span>](http://furius.ca/beancount/doc/contrib)

    Links to codes written by other people that build on top of or that are related to Beancount and/or Ledgerhub.

Indexes<a id="indexes"></a>
---------------------------

This document contains only packages that were discussed or have had an announcement sent to the mailing-list. You will be able to find other packages on public indices:

-   PyPI: You can find a lot of other Beancount-related projects at [<span class="underline">PyPI</span>](https://pypi.org/search/?q=beancount&o=).

-   GitHub: A [<span class="underline">search for "beancount"</span>](https://github.com/search?p=5&q=beancount&ref=opensearch&type=Repositories) as of September 2020 brings up 318 projects.

Books and Articles<a id="books-and-articles"></a>
-------------------------------------------------

[<span class="underline">https://personalfinancespython.com/</span>](https://personalfinancespython.com/) "Managing Personal Finances using Python", a 2020 book on plain-text accounting, and Beancount (Siddhant Goel).

Plugins<a id="plugins"></a>
---------------------------

[<span class="underline">split\_transactions</span>](https://www.google.com/url?q=https%3A%2F%2Fgist.github.com%2Fkljohann%2Faebac3f0146680fd9aa5&sa=D&sntz=1&usg=AFQjCNGn2AkL35onTeXgOQzLzkjVpvLcpg): Johann Klähn [<span class="underline">wrote a plugin</span>](https://groups.google.com/d/msg/beancount/z9sPboW4U3c/1qIIzro4zFoJ) that can split a single transaction into many against a limbo account, as would be done for depreciation.

[<span class="underline">zerosum</span>](https://github.com/redstreet/beancount_plugins_redstreet): redstreet0 [<span class="underline">wrote a plugin</span>](https://groups.google.com/d/msg/beancount/MU6KozsmqGQ/sehD3dqZslEJ) to match up transactions that when taken together should sum up to zero and move them to a separate account.

[<span class="underline">effective\_dates</span>](https://github.com/redstreet/beancount_plugins_redstreet): redstreet0 wrote a plugin to book different legs of a transaction to different dates

[<span class="underline">beancount-plugins</span>](https://github.com/davidastephens/beancount-plugins): Dave Stephens created a repository to share various of his plugins related to depreciation.

[<span class="underline">beancount-plugins-zack</span>](https://github.com/zacchiro/beancount-plugins-zack): Stefano Zacchiroli created this repository to share his plugins.

<span class="underline">b[eancount-oneliner](https://github.com/Akuukis/beancount-oneliner)</span>: Akuukis created a plugin to write an entry in one line ([<span class="underline">PyPi</span>](https://pypi.python.org/pypi/beancount-oneliner/1.0.0)).

[<span class="underline">beancount-interpolate</span>](https://github.com/Akuukis/beancount-interpolate): Akuukis created plugins for Beancount to interpolate transactions (recur, split, depr, spread) ([<span class="underline">PyPi</span>](https://pypi.python.org/pypi/beancount-interpolate)).

[<span class="underline">metadata-spray</span>](https://github.com/seltzered/beancount-plugins-metadata-spray): Add metadata across entries by regex expression rather than having explicit entries (by Vivek Gani).

Tools<a id="tools"></a>
-----------------------

[<span class="underline">alfred-beancount</span>](https://github.com/blaulan/alfred-beancount) (Yue Wu): An add-on to the “Alfred” macOS tool to quickly enter transactions in one’s Beancount file. Supports full account names and payees match.

[<span class="underline">bean-add</span>](https://github.com/simon-v/bean-add) (Simon Volpert): A Beancount transaction entry assistant.

[<span class="underline">hoostus/fincen\_114</span>](https://github.com/hoostus/fincen_114) (Justus Pendleton): An FBAR / FinCEN 114 report generator.

[<span class="underline">ghislainbourgeois/beancount\_portfolio\_allocation</span>](https://github.com/ghislainbourgeois/beancount_portfolio_allocation) ([<span class="underline">Ghislain Bourgeois</span>](https://groups.google.com/d/msgid/beancount/b36d9b67-8496-4021-98ea-0470e5f09e4b%40googlegroups.com?utm_medium=email&utm_source=footer)): A quick way to figure out the asset allocations in different portfolios.

[<span class="underline">hoostus/portfolio-returns</span>](https://github.com/hoostus/portfolio-returns) (Justus Pendleton): portfolio returns calculator

[<span class="underline">costflow/syntax</span>](https://github.com/costflow/syntax) (Leplay Li): A product that allows users to keep plain text accounting from their favorite messaging apps. A syntax for converting one-line message to beancount/\*ledger format.

[<span class="underline">process control chart</span>](https://github.com/hoostus/beancount-control-chart) (Justus Pendleton): Spending relative to portfolio size. [<span class="underline">Thread.</span>](https://groups.google.com/d/msgid/beancount/0cd47f9a-37d6-444e-8516-25e247a9e0cd%40googlegroups.com?utm_medium=email&utm_source=footer)

[<span class="underline">Pinto</span>](https://pypi.org/project/pinto/) (Sean Leavey): Supercharged command line interface for Beancount. Supports automatic insertions of transactions in ledger file.

Importers<a id="importers"></a>
-------------------------------

[<span class="underline">reds importers</span>](https://github.com/redstreet/beancount_reds_importers): Simple importers and tools, mostly ofx based and built on top of \`ofxparse\`. Using ofx (over csv) minimizes data and coding errors, eliminates format breaking changes in csv, allows for automatic imports of balances to generate balance assertions, and imports prices. The goal is to factor out importer code into well maintained common libraries for banks, credit cards, and investment houses, to minimize institution specific code and make writing new importers easy. Look inside the importers/ directory to see a list of institutions supported. More investment, credit card, and banking institutions will be added in the future. Contributions welcome. See [<span class="underline">this thread</span>](https://groups.google.com/d/msg/beancount/nsRCbC6nP4I/Dx5NlTioDq0J) for information about a Yodlee importer.

[<span class="underline">plaid2text</span>](https://github.com/madhat2r/plaid2text): An importer from [<span class="underline">Plaid</span>](http://www.plaid.com/) which stores the transactions to a Mongo DB and is able to render it to Beancount syntax. By Micah Duke.

[<span class="underline">jbms/beancount-import</span>](https://github.com/jbms/beancount-import): A tool for semi-automatically importing transactions from external data sources, with support for merging and reconciling imported transactions with each other and with existing transactions in the beancount journal. The UI is web based. ([<span class="underline">Announcement</span>](https://github.com/jbms/beancount-import), [<span class="underline">link to previous version</span>](https://groups.google.com/d/msg/beancount/YN3xL09QFsQ/qhL8U6JDCgAJ)). By Jeremy Maitin-Shepard.

[<span class="underline">awesome-beancount</span>](https://github.com/wzyboy/awesome-beancount): A collection of importers for Chinese banks + tips and tricks. By [<span class="underline">Zhuoyun Wei</span>](https://github.com/wzyboy).

[<span class="underline">beansoup</span>](https://github.com/fxtlabs/beansoup): Filippo Tampieri is sharing some of his Beancount importers and auto-completer in this project.

[<span class="underline">montaropdf/beancount-importers</span>](https://github.com/montaropdf/beancount-importers/): An importer to extract overtime and vacation from a timesheet format for invoicing customers.

[<span class="underline">siddhantgoel/beancount-dkb</span>](https://github.com/siddhantgoel/beancount-dkb) (Siddhant Goel): importer for DKB CSV files.

[<span class="underline">prabusw/beancount-importer-zerodha</span>](https://github.com/prabusw/beancount-importer-zerodha): Importer for the Indian broker Zerodha.

[<span class="underline">swapi/beancount-utils</span>](https://github.com/swapi/beancount-utils) : Another importer for Zerodha.

[<span class="underline">Dr-Nuke/drnuke-bean</span>](https://github.com/Dr-Nuke/drnuke-bean) (Dr Nuke): An importer for IBKR, based on the flex query (API-like) and one for Swiss PostFinance.

Converters<a id="converters"></a>
---------------------------------

[<span class="underline">plaid2text</span>](https://github.com/madhat2r/plaid2text): Python Scripts to export Plaid transactions and transform them into Ledger or Beancount syntax formatted files.

[<span class="underline">gnucash-to-beancount</span>](https://github.com/henriquebastos/gnucash-to-beancount/): A script from Henrique Bastos to convert a GNUcash SQLite database into an equivalent Beancount input file.

[<span class="underline">debanjum/gnucash-to-beancount</span>](https://github.com/debanjum/gnucash-to-beancount): A fork of the above.

[<span class="underline">andrewStein/gnucash-to-beancount</span>](https://github.com/AndrewStein/gnucash-to-beancount) : A further fork from the above two, which fixes a lot of issues (see [<span class="underline">this thread</span>](https://groups.google.com/d/msg/beancount/MaaASKR1SSI/GX5I8lOkBgAJ)).

[<span class="underline">hoostus/beancount-ynab</span>](https://github.com/hoostus/beancount-ynab) : A converter from YNAB to Beancount.

[<span class="underline">hoostus/beancount-ynab5</span>](https://github.com/hoostus/beancount-ynab5) : Same convert for YNAB from the same author, but for the more recent version 5.

[<span class="underline">ledger2beancount</span>](https://github.com/zacchiro/ledger2beancount/): A script to convert ledger files to beancount. It was developed by Stefano Zacchiroli and Martin Michlmayr.

[<span class="underline">smart\_importer</span>](https://github.com/johannesjh/smart_importer): A smart importer for beancount and fava, with intelligent suggestions for account names. By Johannes Harms.

[<span class="underline">beancount-export-patreon.js</span>](https://gist.github.com/riking/0f0dab2b7761d2f6895c5d58c0b62a66): JavaScript that will export your Patreon transactions so you can see details of exactly who you've been giving money to. By kanepyork@gmail.

[<span class="underline">alensiljak/pta-converters</span>](https://gitlab.com/alensiljak/pta-converters) (Alen Šiljak): GnuCash -&gt; Beancount converter (2019).

[<span class="underline">grostim/Beancount-myTools</span>](https://github.com/grostim/Beancount-myTools) (Timothee Gros): Personal importer tools of the author for French banks.

Price Sources<a id="price-sources"></a>
---------------------------------------

[<span class="underline">hoostus/beancount-price-sources</span>](https://github.com/hoostus/beancount-price-sources) : A Morningstar price fetcher which aggregates multiple exchanges, including non-US ones.

[<span class="underline">andyjscott/beancount-financequote</span>](https://github.com/andyjscott/beancount-financequote) : Finance::Quote support for bean-price.

[<span class="underline">aamerabbas/beancount-coinmarketcap</span>](https://github.com/aamerabbas/beancount-coinmarketcap): Price fetcher for coinmarketcap ([<span class="underline">see post</span>](https://medium.com/@danielcimring/downloading-historical-data-from-coinmarketcap-41a2b0111baf)).

[<span class="underline">grostim/Beancount-myTools/.../iexcloud.py</span>](https://github.com/grostim/Beancount-myTools/blob/master/price/iexcloud.py) : Price fetcher for iexcloud by Timothee Gros.

[<span class="underline">xuhcc/beancount-cryptoassets</span>](https://github.com/xuhcc/beancount-cryptoassets) (Kirill Goncharov): Price sources for cryptocurrencies.

[<span class="underline">xuhcc/beancount-ethereum-importer</span>](https://github.com/xuhcc/beancount-ethereum-importer) (Kirill Goncharov): Ethereum transaction importer for Beancount. Includes a script that downloads transactions from Etherscan and an importer for downloaded transactions.

[<span class="underline">xuhcc/beancount-exchangerates</span>](https://github.com/xuhcc/beancount-exchangerates) (Kirill Goncharov): Price source for [<span class="underline">http://exchangeratesapi.io</span>](http://exchangeratesapi.io).

[<span class="underline">tarioch/beancounttools</span>](https://github.com/tarioch/beancounttools) (Patrick Ruckstuhl): Price sources and importers.

Development<a id="development"></a>
-----------------------------------

[<span class="underline">Py3k type annotations</span>](https://github.com/yegle/beancount-type-stubs): Yuchen Ying is implementing python3 type annotations for Beancount.

Documentation<a id="documentation"></a>
---------------------------------------

[<span class="underline">Beancount Documentation</span>](https://beancount.github.io/docs/) ([<span class="underline">Kirill Goncharov</span>](http://github.com/xuhcc)): Official conversion of the Beancount documentation from Google Docs source to Markdown and HTML. This includes most of the Google Docs documents and is maintained in a Beancount org repo [<span class="underline">here</span>](http://github.com/beancount/docs) by Kirill Goncharov.

[<span class="underline">Beancount Source Code Documentation</span>](http://aumayr.github.io/beancount-docs-static/) ([<span class="underline">Dominik Aumayr</span>](http://github.com/aumayr)): A Sphinx-generated source code documentation of the Beancount codebase. The code to produce this is [<span class="underline">located here</span>](https://github.com/aumayr/beancount-docs).

[<span class="underline">SQL queries for Beancount</span>](http://aumayr.github.io/beancount-sql-queries/) (Dominik Aumayr): Example SQL queries.

[<span class="underline">Beancount —— 命令行复式簿记</span>](https://wzyboy.im/post/1063.html) (Zhuoyun Wei): A tutorial (blog post) in Chinese on how to use Beancount.

[<span class="underline">Managing my personal finances with Beancount</span>](https://alexjj.com/blog/2016/2/managing-my-personal-finances-with-beancount/) (Alex Johnstone)

[<span class="underline">Counting beans—and more—with Beancount</span>](https://lwn.net/SubscriberLink/751874/a38128abb72e45c5/) (LWN)

Interfaces / Web<a id="interfaces-web"></a>
-------------------------------------------

[<span class="underline">fava: A web interface for Beancount</span>](https://github.com/aumayr/fava) (Dominik Aumayr, Jakob Schnitzer): Beancount comes with its own simple web front-end (“bean-web”) intended merely as a thin shell to invoke and display HTML versions of its reports. “Fava” is an alternative web application front-end with more & different features, intended initially as a playground and proof-of-concept to explore a newer, better design for presenting the contents of a Beancount file.

[<span class="underline">Fava Classy Portfolio</span>](https://github.com/seltzered/fava-classy-portfolio) (Vivek Gani): Classy Portfolio is an Extension for Fava, a web interface for the Beancount plaintext accounting software. The extension displays a list of different portfolios (e.g. 'taxable' vs. 'retirement'), with breakdowns using 'asset-class' and 'asset-subclass' metadata labels on commodities.

[<span class="underline">Fava Investor</span>](https://github.com/redstreet/fava_investor) project: Fava\_investor aims to be a comprehensive set of reports, analyses, and tools for investments, for Beancount and Fava. It is a collection of modules, with each module offering a Fava plugin, a Beancount library, and a Beancount based CLI (command line interface). Current modules include: Visual, tree structured asset allocation by class, asset allocation by account, tax loss harvester, cash drag analysis.

[<span class="underline">Fava Miler</span>](https://github.com/redstreet/fava_miler) (RedStreet): Airline miles and rewards points: expiration and value reporting.

[<span class="underline">Fava Envelope</span>](https://github.com/bryall/fava-envelope) (Brian Ryall): A beancount fava extension to add an envelope budgeting capability to fava and beancount. It is developed as a Fava plugin and CLI.

[<span class="underline">scauligi/refried</span>](https://github.com/scauligi/refried) (Sunjay Cauligi): An envelope budgeting plugin for Fava, inspired by YNAB: all expense accounts become individual budgeting categories, budgeting is carried out using transactions to these accounts, and the plugin automaticallyapplies a tag to all rebudget transactions so they can easily be filtered out. Provides budget and account views like YNAB.

Mobile/Phone Data Entry<a id="mobilephone-data-entry"></a>
----------------------------------------------------------

[<span class="underline">Beancount Mobile</span>](https://play.google.com/store/apps/details?id=link.beancount.mobile) App (Kirill Goncharov): A mobile data entry app for Beancount. (Currently only Android is supported.) Repo: [<span class="underline">https://github.com/xuhcc/beancount-mobile</span>](https://github.com/xuhcc/beancount-mobile) ([<span class="underline">Announcement</span>](https://groups.google.com/d/msgid/beancount/014e0879-70e0-4cac-b884-82d8004e1b43%40googlegroups.com?utm_medium=email&utm_source=footer)).

[<span class="underline">http://costflow.io</span>](http://costflow.io/): Plain Text Accounting in WeChat. "*Send a message to our bot in Telegram, Facebook Messenger, Whatsapp, LINE, WeChat, etc. Costflow will transform your message into Beancount / Ledger / hledger format transaction magically. Append the transaction to the file in your Dropbox / Google Drive. With the help of their apps, the file will be synced to your computer.*"
