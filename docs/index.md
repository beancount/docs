<a id="title"></a>Beancount Documentation
=========================================

*This is the top-level page for all documentation related to Beancount.*

[<span class="underline">http://furius.ca/beancount/doc/index</span>](http://furius.ca/beancount/doc/index)

<a id="documentation-for-users"></a>Documentation for Users
-----------------------------------------------------------

[<span class="underline">Command-line Accounting in Context</span>: A motivational document that](01_command_line_accounting_in_context.md) explains what command-line accounting is, *why* I do it, with a simple example of *how* I do it. Read this as an introduction.

[<span class="underline">The Double-Entry Counting Method</span>](02_the_double_entry_counting_method.md): A gentle introduction to the double-entry method, in terms compatible with the assumptions and simplifications that command-line accounting systems make.

[<span class="underline">Installing Beancount</span>](03_installing_beancount.md): Instructions for download and installation on your computer, and software release information.

[<span class="underline">Running Beancount and Generating Reports</span>](04_running_beancount_and_generating_reports.md): How to run the Beancount executables and generate reports with it. This contains technical information for Beancount users.

[<span class="underline">Getting Started with Beancount</span>](05_getting_started_with_beancount.md): A text that explains the basics of how to create, initialize and organize your input file, and the process of declaring accounts and adding padding directives.

[<span class="underline">Beancount Language Syntax</span>](06_beancount_language_syntax.md): A full description of the language syntax with examples. This is the main reference for the Beancount language.

[<span class="underline">Beancount Options Reference</span>](07_beancount_options_reference.md): A description and explanation of all the possible option values.

[<span class="underline">Precision & Tolerances</span>](08_precision_tolerances.md): Transactions and Balance assertions tolerance small amounts of imprecision which are inferred from the context. This document explains how this works.

[<span class="underline">Beancount Query Language</span>](09_beancount_query_language.md): A high-level overview of the bean-query command-line client tool that allows you to extract various tables of data from your Beancount ledger file.

[<span class="underline">Beancount Cheat Sheet</span>](10_beancount_cheat_sheet.md): A single page “cheat sheet” that summarizes the Beancount syntax.

[<span class="underline">How Inventories Work</span>](11_how_inventories_work.md): An explanation of inventories, their representation, and the detail of how lots are matched to positions held in an inventory. This is preliminary reading for the trading doc.

[<span class="underline">Exporting Your Portfolio</span>](12_exporting_your_portfolio.md): How to export your portfolio to external portfolio tracking websites.

[<span class="underline">Tutorial & Example</span>](13_tutorial_example.md): A realistic example ledger file that contains a few years of a hypothetical Beancount user's financial life. This can be used to kick the tires on Beancount and see what reports or its web interface look like. This can give a quick idea of what you can get out of using Beancount.

[<span class="underline">Beancount Mailing-list</span>](https://groups.google.com/forum/#!forum/beancount): Questions and discussions specific to Beancount occur there. Of related interest is also the [<span class="underline">Ledger-CLI Forum</span>](https://groups.google.com/forum/#!forum/ledger-cli) which contains lots of more general discussions and acts as a meta-list for command-line accounting topics.

[<span class="underline">Beancount History and Credits:</span>](14_beancount_history_and_credits.md) A description of the development history of Beancount and a shout out to its contributors.

[<span class="underline">A Comparison of Beancount and Ledger & HLedger</span>](15_a_comparison_of_beancount_and_ledger_hledger.md): A qualitative feature comparison between CLI accounting systems.

[<span class="underline">Fetching Prices in Beancount</span>](16_fetching_prices_in_beancount.md): How to fetch and maintain a price database for your assets using Beancount’s tools.

[<span class="underline">Importing External Data</span>](17_importing_external_data.md): A description of the process of importing data from external files that can be downloaded from financial institutions and the tools and libraries that Beancount provides to automate some of this.

<a id="cookbook-examples"></a>Cookbook & Examples
-------------------------------------------------

*These documents are examples of using the double-entry method to carry out specific tasks. Use these documents to develop an intuition for how to structure your accounts.*

[<span class="underline">Command-line Accounting Cookbook</span>](18_command_line_accounting_cookbook.md): Various examples of how to book many different kinds of financial transactions. This is undoubtedly the best way to build an intuition for how to best use the double-entry method.

[<span class="underline">Trading with Beancount</span>](19_trading_with_beancount.md): An explanation of trading P/L and worked examples of how to deal with various investing and trading scenarios with Beancount. This is a complement to the cookbook.

[<span class="underline">Stock Vesting in Beancount</span>](20_stock_vesting_in_beancount.md): An example that shows how to deal with restricted stock units and vesting events typical of those offered by technology companies & startups.

[<span class="underline">Sharing Expenses with Beancount</span>](21_sharing_expenses_with_beancount.md): A realistic and detailed example of using the double-entry method for sharing expenses for a trip or project with other people.

[<span class="underline">How We Share Expenses</span>](22_how_we_share_expenses.md): A more involved description of a continuous system for (a) sharing expenses between partners when both are contributing and (b) sharing expenses to a specific project (our son) who has a ledger of his own. This describes our real system.

<a id="documentation-for-developers"></a>Documentation for Developers
---------------------------------------------------------------------

[<span class="underline">Beancount Scripting & Plugins</span>](23_beancount_scripting_plugins.md): A guide to writing scripts that load your ledger contents in memory and process the directives, and how to write plugins that transform them.

[<span class="underline">Beancount Design Doc</span>](24_beancount_design_doc.md): Information about the program’s architecture and design choices, code conventions, invariants and methodology. Read this if you want to get a deeper understanding.

[<span class="underline">LedgerHub Design Doc</span>](25_ledgerhub_design_doc.md): The design and architecture of the importing tools and library implemented in [<span class="underline">beancount.ingest</span>](https://bitbucket.org/blais/beancount/src/tip/beancount/ingest/). This used to be a separate project called LedgerHub (now defunct), whose useful parts have been eventually folded into Beancount. This is the somewhat dated original design doc.

[<span class="underline">Source Code</span>](https://bitbucket.org/blais/beancount/src/): The official repository of the Beancount source code lives at [<span class="underline">BitBucket</span>](http://bitbucket.org/blais/beancount/).

[<span class="underline">External Contributions</span>](26_external_contributions.md): A list of plugins, importers and other codes that build on Beancount’s libraries that other people have made and shared.

<a id="enhancement-proposals-discussions"></a>Enhancement Proposals & Discussions
---------------------------------------------------------------------------------

*I occasionally write proposals for enhancements in order to organize and summarize my thoughts before moving forward, and solicit feedback from other users. This is good material to find out what features I’m planning to add, how things work in detail, or compare the differences with other similar software such as Ledger or HLedger.*

[<span class="underline">A Proposal for an Improvement on Inventory Booking</span>](27_a_proposal_for_an_improvement_on_inventory_booking.md): A proposal in which I outline the current state of affairs in Ledger and Beancount regarding inventory booking, and a better method for doing it that will support average cost booking and calculating capital gains without commissions.

[<span class="underline">Settlement Dates in Beancount</span>](28_settlement_dates_in_beancount.md): A discussion of how settlement or auxiliary dates could be used in Beancount, and how they are used in Ledger.

[<span class="underline">Balance Assertions in Beancount</span>](29_balance_assertions_in_beancount.md): A summary of the different semantics for making balance assertions in Beancount and Ledger and a proposal to extend Beancount’s syntax to support more complex assertions.

[<span class="underline">Fund Accounting with Beancount</span>](30_fund_accounting_with_beancount.md): A discussion of fund accounting and how best to go about using Beancount to track multiple funds in a single ledger.

[<span class="underline">Rounding & Precision in Beancount</span>](31_rounding_precision_in_beancount.md): A discussion of important rounding and precision issues for balance checks and a proposal for a better method to infer required precision. ([<span class="underline">Implemented</span>](08_precision_tolerances.md))

<a id="external-links"></a>External Links
-----------------------------------------

*Documents, links, blog entries, writings, etc. about Beancount written by other authors.\]*

[<span class="underline">Beancount Source Code Documentation</span>](http://aumayr.github.io/beancount-docs-static/) (Dominik Aumayr): Sphinx-generated source code documentation of the Beancount codebase. The code to produce this is [<span class="underline">located here</span>](https://github.com/aumayr/beancount-docs).

[<span class="underline">Beancount ou la comptabilité pour les hackers</span>](http://blog.deguet.fr/beancount-comptabilite-pour-hackers/) (Cyril Deguet): An overview blog entry (in french).

<a id="about-this-documentation"></a>About this Documentation
-------------------------------------------------------------

You may have noticed that I’m using [<span class="underline">Google Docs</span>](https://docs.google.com/). I realize that this is unusual for an open source project. If you [<span class="underline">take offense to this</span>](https://groups.google.com/d/msg/ledger-cli/u648SA1o-Ek/yom_P38FCAAJ), so you know, I do like text formats too: in graduate school I used [<span class="underline">LaTeX</span>](http://www.latex-project.org/) extensively, and for the last decade I was in love with the [<span class="underline">reStructuredText</span>](http://docutils.sourceforge.net) format, I even wrote Emacs’ support for it. But something happened around 2013: [<span class="underline">Google Docs</span>](https://docs.google.com/) became good enough to write solid technical documentation and I’ve begun enjoying its revision and commenting facilities extensively: I am hooked, I love it. For users to be able to suggest a correction or place a comment in context is an incredibly useful feature that helps improve the quality of my writing a lot more than patches or comments on a mailing-list. It also gives users a chance to point out passages that need improvement. I have already received orders of magnitude more feedback on documentation than on any of my other projects; it works.

It also looks really *good*, and this is helping motivate me to write more and better. I think maybe I’m falling in love again with WYSIWYG... Don’t take me wrong: LaTeX and no-markup formats are great, but the world is changing and it is more important to me to have community collaboration and a living document than a crufty TeX file slowly aging in my repository. My aim is to produce quality text that is easy to read, that prints nicely, and most especially these days, that can render well on a mobile device or a tablet so you can read it anywhere. I’m also able to edit it while I’m on the go, which is fun for jotting down ideas or making corrections. Finally, Google Docs has an API that provides access to the doc, so should it be needed, I could eventually download the meta-data and convert it all to another format. I don’t like everything about it, but what it offers, I really do like.

If you want to leave comments, I’d appreciate if you can **log into your Google account** while you read, so that your name appears next to your comment. Thank you!

—[<span class="underline">Martin Blais</span>](mailto:blais@furius.ca)
