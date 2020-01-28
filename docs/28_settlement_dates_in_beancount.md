Settlement Dates & Transfer Accounts in Beancount<a id="title"></a>
===================================================================

Martin Blais, July 2014

[<span class="underline">http://furius.ca/beancount/doc/proposal-dates</span>](http://furius.ca/beancount/doc/proposal-dates)

> [<span class="underline">Motivation</span>](#motivation)
>
> [<span class="underline">Proposal Description</span>](#_1t2cyy3ee86k)
>
> [<span class="underline">Remaining Questions</span>](#remaining-questions)
>
> [<span class="underline">Previous Work</span>](#_svp0j511dy5a)
>
> [<span class="underline">Ledger Effective and Auxiliary Dates</span>](#ledger-effective-and-auxiliary-dates)
>
> [<span class="underline">References</span>](#references)

Motivation<a id="motivation"></a>
---------------------------------

When a trade executes in an investment account, there is most often a delay between the date that the transaction is carried out (the “transaction date”) and the date that the funds are deposited in an associated cash account (the “settlement date”). This makes imported balance assertions sometimes requiring the fudging of their dates, and sometimes they can even be impossible. This document proposes the addition of an optional “settlement date” to be attached to a transaction or a posting, and associated semantics for how to deal with the problem.

Proposal Description<a id="proposal-description"></a>
-----------------------------------------------------

### Settlement Dates<a id="settlement-dates"></a>

In the first implementation of Beancount I used to have two dates attached to a transaction, but I never did anything with them. The alternate date would get attached but was ignored thereafter. The meaning of it is that it should have split the transaction into two, with some sort of transfer account, that might have been useful semantics, I never developed it.

Something like this as input:

    2014-06-23=2014-06-28 * "Sale"
       Assets:ScottTrade:GOOG    -10 GOOG {589.00 USD}
       S Assets:ScottTrade:Cash

where the “S” posting flag marks the leg “to be postponed to the settlement date.”

Alternatively, you could attach the date to a posting:

    2014-06-23 * "Sale"
       Assets:ScottTrade:GOOG    -10 GOOG {589.00 USD}
       2014-06-28 Assets:ScottTrade:Cash

Both of the above syntax proposals allow you to specify which postings are meant to be postponed to settlement. The second one is more flexible, as each posting could potentially have a different date, but the more constrained syntax of the first would create less complications.

Either of these could get translated to multiple transactions with a transfer account to absorb the pending amount:

    2014-06-23 * "Sale" ^settlement-3463873948
       Assets:ScottTrade:GOOG    -10 GOOG {589.00 USD}
       Assets:ScottTrade:Transfer

    2014-06-28 * "Sale" ^settlement-3463873948
       Assets:ScottTrade:Transfer
       Assets:ScottTrade:Cash        5890.00 USD

So far, I’ve been getting away with fudging the dates on balance assertions where necessary. I have relatively few sales, so this hasn’t been a big problem so far. I’m not convinced it needs a solution yet, maybe the best thing to do is just to document how to deal with the issue when it occurs.

Maybe someone can convince me otherwise.

### Transfer Accounts<a id="transfer-accounts"></a>

In the previous section, we discuss a style whereby a single entry moving money between two accounts contains two dates and results in two separate entries. An auxiliary problem, which is related in its solution, is how to carry out the reverse operation, that is, how to *merge* two separate entries posting to a common transfer account (sometimes called a “[<span class="underline">suspense account</span>](https://en.wikipedia.org/wiki/Suspense_account)”).

For example, a user may want to input the two sides of a transaction separately, e.g. by running import scripts on separate input files, and instead of having to reconcile and merge those by hand, we would want to explicitly support this by identifying matching transactions to these transfer accounts and creating a common link between them.

Most importantly, we want to be able to easily identify which of the transactions is not matched on the other side, which indicates missing data.

-   There is a prototype of this under [<span class="underline">beancount.plugins.tag\_pending</span>](https://bitbucket.org/blais/beancount/src/tip/src/python/beancount/plugins/tag_pending.py?at=default).

-   Also see redstreet0’s “[<span class="underline">zerosum</span>](https://groups.google.com/d/msgid/beancount/8adbb83d-a7c7-476a-97ca-d600d110db20%40googlegroups.com?utm_medium=email&utm_source=footer)” plugin from [<span class="underline">this thread</span>](https://groups.google.com/d/msgid/beancount/8adbb83d-a7c7-476a-97ca-d600d110db20%40googlegroups.com?utm_medium=email&utm_source=footer).

Remaining Questions<a id="remaining-questions"></a>
---------------------------------------------------

*How do we determine a proper transfer account name? Is a subaccount a reasonable approach? What if a user would like to have a single global limbo account?*

    TODO

*Does this property solve the problem of making balance assertions between trade and settlement?*

    TODO [Write out a detailed example]

*Any drawbacks?*

    TODO

*How does this affect the balance sheet and income statement, if any? Is it going to be obvious to users what the amounts in these limbo/transfer accounts are?*

    TODO

Unrooting Transactions<a id="unrooting-transactions"></a>
---------------------------------------------------------

A wilder idea would be to add an extra level in the transaction-posting hierarchy, adding the capability to group multiple partial transactions, and move the balancing rule to that level. Basically, two transactions input separately and then grouped - by some rule, or trivially by themselves - could form a new unit of balance rule.

That would be a much more demanding change on the schema and on the Beancount design but would allow to natively support partial transactions, keeping their individual dates, descriptions, etc. Maybe that's a better model? Consider the advantages.

Previous Work<a id="previous-work"></a>
---------------------------------------

### Ledger Effective and Auxiliary Dates<a id="ledger-effective-and-auxiliary-dates"></a>

Ledger has the concept of “[<span class="underline">auxiliary dates</span>](http://ledger-cli.org/3.0/doc/ledger3.html#Auxiliary-dates)”. The way these work is straightforward: any transaction may have a second date, and the user can select at runtime (with --aux-date) whether the main date or the auxiliary dates are meant to be used.

It is unclear to me how this is meant to be used in practice, in the presence of balance assertions. Without balance assertions, I can see how it would just work: you’d render everything with settlement dates only. This would probably only make sense for specific reports.

I would much rather keep a single semantic for the set of transactions that gets parsed in; the idea that the meaning of the transactions varies depending on the invocation conditions would set a precedent in Beancount, I’d prefer not to break this nice property, so by default I’d prefer to avoid implementing this solution.

Auxiliary dates are also known as “[<span class="underline">effective dates</span>](http://ledger-cli.org/3.0/doc/ledger3.html#Effective-Dates)” and can be associated with each individual posting. Auxiliary dates are secondary to the the “primary date” or the “actual date”, being the posting date of the record):

    2008/10/16 * (2090) Bountiful Blessings Farm
        Expenses:Food:Groceries                  $ 37.50  ; [=2008/10/01]
        Expenses:Food:Groceries                  $ 37.50  ; [=2008/11/01]
        Expenses:Food:Groceries                  $ 37.50  ; [=2008/12/01]
        Expenses:Food:Groceries                  $ 37.50  ; [=2009/01/01]
        Expenses:Food:Groceries                  $ 37.50  ; [=2009/02/01]
        Expenses:Food:Groceries                  $ 37.50  ; [=2009/03/01]
        Assets:Checking

The original motivation for this was for budgeting, allow one to move accounting of expenses to neighboring budget periods in order to carry over actual paid amounts to those periods. Bank amounts in one month could be set against a budget from the immediately preceding or following month, as needed. (Note: John Wiegley)

This is similar to one of the syntaxes I’m suggesting above—letting the user specify a date for each posting—but the other postings are not split as independent transactions. The usage of those dates are similarly triggered by a command-line option (--effective). I’m assuming that the posting on the checking account above occurs at once at 2008/10/16, regardless of reporting date. Let’s verify this:

    $ ledger -f settlement1.lgr reg checking --effective
    08-Oct-16 Bountiful Blessings.. Assets:Checking           $ -225.00    $ -225.00

That’s what I thought. This works, but a problem with this approach is that any balance sheet drawn between 2008/10/01 (the earliest effective date) and 2009/03/01 (the latest effective date) would not balance. Between those dates, some amounts are “in limbo” and drawing up a balance sheet at one of those dates would not balance.

This would break an invariant in Beancount: we require that you should always be able to draw a balance sheet at any point in time, and any subset of transactions should balance. I would rather implement this by splitting this example transaction into many other ones, as in the proposal above, moving those temporary amounts living in limbo in an explicit “limbo” or “transfer” account, where each transaction balances. Moreover, this step can be implemented as a transformation stage, replacing the transaction with effective dates by one transaction for each posting where the effective date differs from the transaction’s date (this could be enabled on demand via a plugin).

### GnuCash<a id="gnucash"></a>

*TODO(blais) - How is this handled in GnuCash and other GUI systems? Is there a standard account method?*

References<a id="references"></a>
---------------------------------

The IRS [<span class="underline">requires you to use the trade date and NOT the settlement date</span>](http://www.irs.gov/publications/p17/ch14.html) for tax reporting; from the IRS Publication 17:

> **Securities traded on established market.** For securities traded on an established securities market, your holding period begins the day after the trade date you bought the securities, and ends on the trade date you sold them.
>
> <img src="28_settlement_dates_in_beancount/media/1336b54a60f8aa4b92957260378207d6479e7c39.gif" style="width:0.5625in;height:0.5625in" />Do not confuse the trade date with the settlement date, which is the date by which the stock must be delivered and payment must be made.
>
> **Example.**
>
> You are a cash method, calendar year taxpayer. You sold stock at a gain on December 30, 2013. According to the rules of the stock exchange, the sale was closed by delivery of the stock 4 trading days after the sale, on January 6, 2014. You received payment of the sales price on that same day. Report your gain on your 2013 return, even though you received the payment in 2014. The gain is long term or short term depending on whether you held the stock more than 1 year. Your holding period ended on December 30. If you had sold the stock at a loss, you would also report it on your 2013 return.

### Threads<a id="threads"></a>

-   [<span class="underline">An interesting "feature by coincidence"</span>](https://groups.google.com/d/msg/ledger-cli/ooxbPVRinSs/ymkRCerhxjcJ)

-   [<span class="underline">First Opinions, Coming from Ledger</span>](https://groups.google.com/d/msg/beancount/z9sPboW4U3c/UfJbIVzwmpMJ)
