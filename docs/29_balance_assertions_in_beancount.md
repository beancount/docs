Balance Assertions in Beancount
===============================

Martin Blais, July 2014

[<span class="underline">http://furius.ca/beancount/doc/proposal-balance</span>](http://furius.ca/beancount/doc/proposal-balance)

*This document summarizes the different kinds of semantics for balance assertions in all command-line accounting systems and proposes new syntax for total and file-order running assertions in Beancount.*

> [<span class="underline">Motivation</span>](#motivation)
>
> [<span class="underline">Partial vs. Complete Assertions</span>](#partial-vs.-complete-assertions)
>
> [<span class="underline">File vs. Date Assertions</span>](#file-vs.-date-assertions)
>
> [<span class="underline">Ordering & Ambiguity</span>](#ordering-ambiguity)
>
> [<span class="underline">Intra-Day Assertions</span>](#intra-day-assertions)
>
> [<span class="underline">Beginning vs. End of Day</span>](#beginning-vs.-end-of-day)
>
> [<span class="underline">Status</span>](#status)
>
> [<span class="underline">Proposal</span>](#proposal)
>
> [<span class="underline">File Assertions</span>](#file-assertions)
>
> [<span class="underline">Complete Assertions</span>](#complete-assertions)

Motivation
----------

Both Beancount and Ledger implement *balance assertions.* These provide the system with checkpoints it can use to verify the integrity of the data entry[1].

Traditional accounting principles state that a user may never change the past—correcting the past involves inserting new entries to undo past mistakes[2]—but we in the command-line accounting community take issue with that: we want to remain able to reconstruct the past and more importantly, to correct past mistakes at the site of their original data entry. Yes, we are dilettantes but we are bent on simplifying the process of bookkeeping by challenging existing concepts and think that this is perfectly reasonable, as long as it does not break known balances. These known balances are what we provide via balance assertions.

Another way to look at these balance assertions, is that they are simply the bottom line amounts reported on various account statements, as exemplified in the figure below.

Following [<span class="underline">this thread</span>](https://groups.google.com/forum/#!topic/ledger-cli/vwkrPh74NFI), we established that there were differing interpretations of balance assertions in the current versions of Ledger (3.0) and Beancount (2.0b).

<img src="29_balance_assertions_in_beancount/media/539ac8accaa66eeb45ed7865fcad381fa35af295.png" alt="balance-statement-1.png" style="width:6.5in;height:3.20833in" />

Partial vs. Complete Assertions
-------------------------------

An assertion in Beancount currently looks like this:

    2012-02-04 balance Assets:CA:Bank:Checking    417.61 CAD

The meaning of this directive is: “please assert that the inventory of account ‘Assets:CA:Bank:Checking’ contains exactly 417.61 units of CAD at the end of February 3, 2012” (so it’s dated on the 4th because in Beancount balance assertions are specified at the beginning of the date). It says nothing about other commodities in the account’s inventory. For example, if the account contains units of “USD”, those are unchecked. We will call this interpretation a **partial balance assertion** or **single-commodity assertion**.

An alternative assertion would be exhaustive: “please assert that the inventory of account ‘Assets:CA:Bank:Checking’ contains only 417.61 units of CAD at the end of February 3, 2012.” We call this a **complete balance assertion**. In order to work, this second type of assertion would have to support the specification of the full contents of an inventory. This is currently not supported.

Further note that we are not asserting the cost basis of an inventory, just the number of units.

File vs. Date Assertions
------------------------

There are two differing interpretations and implementations of the running balances for assertions:

-   Beancount first sorts all the directives and verifies the balance at the *beginning* of the date of the directive. In the previous example, that is “*the balance before any transactions on 2012-02-04 are applied.”* We will call this **date assertions** or **date-based assertions**.

-   Ledger keeps a running balance of each account’s inventory during its parsing phase and performs the check *at the site of the assertion in the file.* We will call this **file assertions** or **file-order,** or **file-based assertions**. This kind of assertion has no date associated with it (this is slightly misleading in Ledger because of the way assertions are specified, as attached to a transaction’s posting, which appears to imply that they occur on the transaction date, but they don’t, they strictly apply to the file location).

### Ordering & Ambiguity

An important difference between those two types of assertions is that file-based assertions are not order-independent. For example, take the following input file:

    ;; Credit card account
    2014/05/01 opening
      Liabilities:CreditCard    $-1000.00
      Expenses:Opening-Balances

    2014/05/12 dinner
      Liabilities:CreditCard    $-74.20
      Expenses:Restaurant

    ;; Checking account
    2014/06/05 salary
      Assets:Checking            $4082.87
      Income:Salary

    2014/06/05 cc payment
      Assets:Checking            $-1074.20 = $3008.67
      Liabilities:CreditCard     = $0

If you move the credit card payment up to the credit card account section, the same set of transactions fails:

    ;; Credit card account
    2014/05/01 opening
      Liabilities:CreditCard    $-1000.00
      Expenses:Opening-Balances

    2014/05/12 dinner
      Liabilities:CreditCard    $-74.20
      Expenses:Restaurant

    2014/06/05 cc payment
      Assets:Checking            $-1074.20 = $3008.67
      Liabilities:CreditCard     = $0

    ;; Checking account
    2014/06/05 salary
      Assets:Checking            $4082.87
      Income:Salary

This subtle problem could be difficult for beginners to understand. Moving the file assertion to its own, undated directive might be more indicative syntax of its semantics, something that would look like this:

    balance Assets:Checking = $3008.67

The absence of a date indicates that the check is not applied at a particular point in time.

### Intra-Day Assertions

On the other hand, date-based assertions, because of their order-independence, preclude intra-day assertions, that is, a balance assertion that occurs *between* two postings on the same account during the same day.

Beancount does not support intra-day assertions at the moment.

Note despite this shortcoming, this has not been much of a problem, because it is often possible to fudge the date where necessary by adding or removing a day, or even just skipping an assertion where it would be impossible (skipping assertions is not a big deal, as they are optional and their purpose is just to provide certainty. As long as you have one that appears some date after the skipped one, it isn’t much of an issue).

It would be nice to find a solution to intra-day assertions for date-based assertions, however. One interesting idea would be to extend the semantics to apply the balance in file order within the set of all transactions directly before and after the balance check that occur on the same date as the balance check, for example, this would balance:

    2013-05-05 balance Assets:Checking    100 USD

    2013-05-20 * “Interest payment”
      Assets:Checking           12.01 USD
      Income:Interest

    2013-05-20 balance Assets:Checking    121.01 USD

    2013-05-20 * “Check deposit”
      Assets:Checking           731.73 USD
      Assets:Receivable

The spell would be broken as soon as a directive would appear at a different date.

Another idea would be to always sort the balance assertions in file-order as the second sort key (after the date) and apply them as such. I’m not sure this would be easy to understand though.

### Beginning vs. End of Day

Finally, just for completeness, it is worth mentioning that date assertions have to have well-defined semantics regarding *when* they apply during the day. In Beancount, they currently apply at the beginning of the day.

It might be worthwhile to provide an alternate version of date-based assertions that applies at the end of the day, e.g. “balance\_end”. Beancount v1 used to have this (“check\_end”) but it was removed in the v2 rewrite, as it wasn’t clear it would be really needed. The simplicity of a single meaning for balance assertions is nice too.

Status
------

[<span class="underline">Ledger</span>](http://ledger-cli.org) 3.0 currently supports only partial file-order assertions, on transactions.

[<span class="underline">Beancount</span>](http://furius.ca/beancount/) 2.0 currently supports only partial date-based assertions at the beginning of the day.

Proposal
--------

I propose the following improvements to Beancount’s balance assertions.

### File Assertions

File assertions should be provided as a plugin. They would look like this:

    2012-02-03 file_balance Assets:CA:Bank:Checking    417.61 CAD

Ideally, in order to make it clear that they apply strictly in file order, they would not have a date, something like this:

    file_balance Assets:CA:Bank:Checking    417.61 CAD

But this breaks the regularity of the syntax for all other directives. It also complicates an otherwise very regular and simple parser just that much more… *all* other directives begin with a date and a word, and all other lines are pretty much ignored. It would be a bit of a departure from this. Finally, it would still be nice to have a date just to insert those directives somewhere in the rendered journal. So I’m considering keeping a date for it. If you decide to use those odd assertions, you should know what they mean.

I also don’t like the idea of attaching assertions to transactions; transaction syntax is already busy enough, it is calling to remain simple. This should be a standalone directive that few people use.

In order to implement this, the plugin would simply resort all the directives according to their file location only (using the fileloc attribute of entries), disregarding the date, and recompute the running balances top to bottom while applying the checks. This can entirely be done via post-processing, like date-based assertions, without disturbing any of the other processing.

Moreover, another advantage of doing this in a plugin is that people who don’t use this directive won’t have to pay the cost of calculating these inventories.

### Complete Assertions

Complete assertions should be supported in Beancount by the current balance assertion directive. They aren’t very important but are potentially useful.

Possible syntax ideas:

    2012-02-03 balance* Assets:CA:Bank:Checking        417.61 CAD, 162 USD

    2012-02-03 balance Assets:CA:Bank:Checking       = 417.61 CAD, 162 USD

    2012-02-03 balance full Assets:CA:Bank:Checking    417.61 CAD, 162 USD

    2012-02-03 balance 
      Assets:CA:Bank:Checking    417.61 CAD
      Assets:CA:Bank:Checking       162 USD

I’m still undecided which is best. So far it seems a matter of taste.

[1] As far as we know, the notion of inputting an explicit expected amount is unique to command-line accounting systems. Other systems “reconcile” by freezing changes in the past.

[2] There are multiple reasons for this. First, in pre-computer times, accounting was done using books, and recomputing running balances manually would have involved making multiple annoying corrections to a book. This must have been incredibly inconvenient, and inserting correcting entries at the current time is a lot easier. Secondly, if your accounting balances are used to file taxes, changing some of the balances retroactively makes it difficult to go back and check the detail of reported amounts in case of an audit. This problem also applies to our context, but whether a past correction should be allowed is a choice that depends on the context and the particular account, and we leave it up to the user to decide whether it should be allowed.
