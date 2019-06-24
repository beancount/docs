External Contributions to Beancount
===================================

[<span class="underline">Martin Blais</span>](mailto:blais@furius.ca) - Updated: April 2016

[<span class="underline">http://furius.ca/beancount/doc/contrib</span>](http://furius.ca/beancount/doc/contrib)

*Links to codes written by other people that build on top of  
or that are related to Beancount and/or Ledgerhub.*

Plugins
-------

[<span class="underline">split\_transactions</span>](https://www.google.com/url?q=https%3A%2F%2Fgist.github.com%2Fkljohann%2Faebac3f0146680fd9aa5&sa=D&sntz=1&usg=AFQjCNGn2AkL35onTeXgOQzLzkjVpvLcpg): Johann Klähn [<span class="underline">wrote a plugin</span>](https://groups.google.com/d/msg/beancount/z9sPboW4U3c/1qIIzro4zFoJ) that can split a single transaction into many against a limbo account, as would be done for depreciation.

[<span class="underline">zerosum</span>](https://github.com/redstreet/beancount_plugins_redstreet): redstreet0 [<span class="underline">wrote a plugin</span>](https://groups.google.com/d/msg/beancount/MU6KozsmqGQ/sehD3dqZslEJ) to match up transactions that when taken together should sum up to zero and move them to a separate account.

[<span class="underline">effective\_dates</span>](https://github.com/redstreet/beancount_plugins_redstreet): redstreet0 wrote a plugin to book different legs of a transaction to different dates

[<span class="underline">depreciation</span>](https://bitbucket.org/snippets/happyalu/EAMgj/beancount-automated-depreciation-plugin): [<span class="underline">Alok Parlikar</span>](https://plus.google.com/u/0/+AlokParlikar/posts) [<span class="underline">wrote a plugin</span>](https://bitbucket.org/snippets/happyalu/EAMgj/beancount-automated-depreciation-plugin) to automatically add entries at the EOY for the depreciation of assets.

[<span class="underline">beancount-plugins</span>](https://github.com/davidastephens/beancount-plugins): Dave Stephens created a repository to share various of his plugins related to depreciation.

[<span class="underline">beancount-plugins-zack</span>](https://github.com/zacchiro/beancount-plugins-zack): Stefano Zacchiroli created this repository to share his plugins.

<span class="underline">b[eancount-oneliner](https://github.com/Akuukis/beancount-oneliner)</span>: Akuukis created a plugin to write an entry in one line ([<span class="underline">PyPi</span>](https://pypi.python.org/pypi/beancount-oneliner/1.0.0)).

[<span class="underline">beancount-interpolate</span>](https://github.com/Akuukis/beancount-interpolate): Akuukis created plugins for Beancount to interpolate transactions (recur, split, depr, spread) ([<span class="underline">PyPi</span>](https://pypi.python.org/pypi/beancount-interpolate)).

[<span class="underline">metadata-spray</span>](https://github.com/seltzered/beancount-plugins-metadata-spray): Add metadata across entries by regex expression rather than having explicit entries (by Vivek Gani).

Tools
-----

[<span class="underline">alfred-beancount</span>](https://github.com/blaulan/alfred-beancount) (Yue Wu): An add-on to the “Alfred” macOS tool to quickly enter transactions in one’s Beancount file. Supports full account names and payees match.

[<span class="underline">bean-add</span>](https://github.com/simon-v/bean-add) (Simon Volpert): A Beancount transaction entry assistant.

[<span class="underline">hoostus/fincen\_114</span>](https://github.com/hoostus/fincen_114) (Justus Pendleton): A FBAR / FinCEN 114 report generator.

[<span class="underline">ghislainbourgeois/beancount\_portfolio\_allocation</span>](https://github.com/ghislainbourgeois/beancount_portfolio_allocation) ([<span class="underline">Ghislain Bourgeois</span>](https://groups.google.com/d/msgid/beancount/b36d9b67-8496-4021-98ea-0470e5f09e4b%40googlegroups.com?utm_medium=email&utm_source=footer)): A quick way to figure out the asset allocations in different portfolios.

[<span class="underline">hoostus/portfolio-returns</span>](https://github.com/hoostus/portfolio-returns) (Justus Pendleton): portfolio returns calculator

Importers
---------

[<span class="underline">yodlee importer</span>](https://bitbucket.org/redstreet/ledgerhub/commits/5cad3e7495479b1598585a3cfcdd9a06051efcc1): redstreet0 wrote an importer for fetching data from the Yodlee account aggregator. Apparently you can get free access [<span class="underline">as per this thread</span>](https://groups.google.com/d/msg/beancount/nsRCbC6nP4I/Dx5NlTioDq0J).

[<span class="underline">plaid2text</span>](https://github.com/madhat2r/plaid2text): An importer from [<span class="underline">Plaid</span>](http://www.plaid.com/) which stores the transactions to a Mongo DB and is able to render it to Beancount syntax. By Micah Duke.

[<span class="underline">jbms/beancount-import</span>](https://github.com/jbms/beancount-import): A tool for semi-automatically importing transactions from external data sources, with support for merging and reconciling imported transactions with each other and with existing transactions in the beancount journal. The UI is web based. ([<span class="underline">Announcement</span>](https://github.com/jbms/beancount-import), [<span class="underline">link to previous version</span>](https://groups.google.com/d/msg/beancount/YN3xL09QFsQ/qhL8U6JDCgAJ)). By Jeremy Maitin-Shepard.

[<span class="underline">awesome-beancount</span>](https://github.com/wzyboy/awesome-beancount): A collection of importers for Chinese banks + tips and tricks. By [<span class="underline">Zhuoyun Wei</span>](https://github.com/wzyboy).

[<span class="underline">beansoup</span>](https://bitbucket.org/fxt/beansoup/): Filippo Tampieri is sharing some of his Beancount importers and auto-completer in this project.

[<span class="underline">montaropdf/beancount-importers</span>](https://github.com/montaropdf/beancount-importers/): An importer to extract overtime and vacation from a timesheet format for invoicing customers.

[<span class="underline">siddhantgoel/beancount-dkb</span>](https://github.com/siddhantgoel/beancount-dkb) (Siddhant Goel): importer for DKB CSV files.

Converters
----------

<span class="underline">p[laid2text](https://github.com/madhat2r/plaid2text)</span>: Python Scripts to export Plaid transactions and transform them into Ledger or Beancount syntax formatted files.

[<span class="underline">gnucash-to-beancount</span>](https://github.com/henriquebastos/gnucash-to-beancount/): A script from Henrique Bastos to convert a GNUcash SQLite database into an equivalent Beancount input file.

[<span class="underline">debanjum/gnucash-to-beancount</span>](https://github.com/debanjum/gnucash-to-beancount): A fork of the above.

[<span class="underline">andrewStein/gnucash-to-beancount</span>](https://github.com/AndrewStein/gnucash-to-beancount) : A further fork from the above two, which fixes a lot of issues (see [<span class="underline">this thread</span>](https://groups.google.com/d/msg/beancount/MaaASKR1SSI/GX5I8lOkBgAJ)).

[<span class="underline">hoostus/beancount-ynab</span>](https://github.com/hoostus/beancount-ynab) : A converter from YNAB to Beancount.

[<span class="underline">ledger2beancount</span>](https://github.com/zacchiro/ledger2beancount/): A script to convert ledger files to beancount. It was developed by Stefano Zacchiroli and Martin Michlmayr.

[<span class="underline">smart\_importer</span>](https://github.com/johannesjh/smart_importer): A smart importer for beancount and fava, with intelligent suggestions for account names. By Johannes Harms.

[<span class="underline">beancount-export-patreon.js</span>](https://gist.github.com/riking/0f0dab2b7761d2f6895c5d58c0b62a66): JavaScript that will export your Patreon transactions so you can see details of exactly who you've been giving money to. By kanepyork@gmail.

[<span class="underline">alensiljak/pta-converters</span>](https://gitlab.com/alensiljak/pta-converters) (Alen Šiljak): GnuCash -&gt; Beancount converter (2019).

Price Sources
-------------

[<span class="underline">hoostus/beancount-price-sources</span>](https://github.com/hoostus/beancount-price-sources) : A Morningstar price fetcher which aggregates multiple exchanges, including non-US ones.

[<span class="underline">andyjscott/beancount-financequote</span>](https://github.com/andyjscott/beancount-financequote) : Finance::Quote support for bean-price.

[<span class="underline">aamerabbas/beancount-coinmarketcap</span>](https://github.com/aamerabbas/beancount-coinmarketcap): Price fetcher for coinmarketcap ([<span class="underline">see post</span>](https://medium.com/@danielcimring/downloading-historical-data-from-coinmarketcap-41a2b0111baf)).

Development
-----------

[<span class="underline">Py3k type annotations</span>](https://github.com/yegle/beancount-type-stubs): Yuchen Ying is implementing python3 type annotations for Beancount.

Documentation
-------------

[<span class="underline">Beancount Source Code Documentation</span>](http://aumayr.github.io/beancount-docs-static/) (Dominik Aumayr): Sphinx-generated source code documentation of the Beancount codebase. The code to produce this is [<span class="underline">located here</span>](https://github.com/aumayr/beancount-docs).

[<span class="underline">SQL queries for Beancount</span>](http://aumayr.github.io/beancount-sql-queries/) (Dominik Aumayr): Example SQL queries.

[<span class="underline">Beancount —— 命令行复式簿记</span>](https://wzyboy.im/post/1063.html) (Zhuoyun Wei): A tutorial (blog post) in Chinese on how to use Beancount.

[<span class="underline">Managing my personal finances with Beancount</span>](https://alexjj.com/blog/2016/2/managing-my-personal-finances-with-beancount/) (Alex Johnstone)

[<span class="underline">Counting beans—and more—with Beancount</span>](https://lwn.net/SubscriberLink/751874/a38128abb72e45c5/) (LWN)

Interfaces / Web
----------------

[<span class="underline">fava: A web interface for Beancount</span>](https://github.com/aumayr/fava) (Dominik Aumayr): Beancount comes with its own simple web front-end (“bean-web”) intended merely as a thin shell to invoke and display HTML versions of its reports. “Fava” is an alternative web application front-end with more & different features, intended initially as a playground and proof-of-concept to explore a newer, better design for presenting the contents of a Beancount file.
