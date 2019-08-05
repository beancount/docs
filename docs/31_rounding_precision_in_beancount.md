<a id="title"></a>Proposal: Rounding & Precision in Beancount
=============================================================

[<span class="underline">Martin Blais</span>](http://plus.google.com/+MartinBlais), October 2014

*This document describes the problem of rounding errors on  
Beancount transactions and how they are handled. It also includes*

*a proposal for better handling precision issues in Beancount.*

<a id="motivation"></a>Motivation
---------------------------------

### <a id="balancing-precision"></a>Balancing Precision

Balancing transactions cannot be done precisely. This has been [<span class="underline">discussed on the Ledger mailing-list before</span>](https://groups.google.com/d/msg/ledger-cli/m-TgILbfrwA/YjkmOM3LHXIJ). It is necessary to allow for some tolerance on the amounts used to balance a transaction.

This need is clear when you consider that inputting numbers in a text file implies a limited decimal representation. For example, if you’re going to multiply a number of units and a cost, say both written down with 2 fractional digits, you might end up with a number that has 4 fractional digits, and then you need to compare that result with a cash amount that would typically be entered with only 2 fractional digits, something like this example:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       4.27 RGAGX {53.21 USD} 
      Assets:Investments:Cash     -227.21 USD

If you calculate it, the first posting’s precise balance amount is 227.2067 USD, not 227.21 USD. However, the broker company managing the investment account will apply rounding to the closest cent for the cash withdrawal, and the rounded amount is the correct one to be used. This transaction has to balance; we need to allow for some looseness somehow.

The great majority of the cases where mathematical operations occur involve the conversion from a number of units and a price or a cost to a corresponding cash value (e.g., units x cost = total cost). Our task in representing transactional information is the replication of operations that take place mostly in institutions. These operations always involve the rounding of numbers for units and currencies (banks do apply stochastic rounding), and the *correct* numbers to be used from the perspective of these institutions, and from the perspective of the government, are indeed the *rounded* numbers themselves. It is a not a question of mathematical purity, but one of practicality, and our system should do the same that banks do. Therefore, I think that we should always post the rounded numbers to accounts. Using rational numbers is not a limitation in that sense, but we must be careful to store rounded numbers where it matters.

### <a id="automatic-rounding"></a>Automatic Rounding

Another related issue is that of automatically rounding amounts for interpolated numbers. Let’s take our original problematic example again:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       4.27 RGAGX {53.21 USD} 
      Assets:Investments:Cash     ;; Interpolated posting = -227.2067 USD

Here the amount from the second posting is interpolated from the balance amount for the first posting. Ideally, we should find a way to specify how it should round to 2 fractional digits of precision.

Note that this affects interpolated prices and costs too:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       4.27 RGAGX {USD} 
      Assets:Investments:Cash     -227.21 USD

Here, the cost is intended to be automatically calculated from the cash legs: 227.21 / 4.27 = 53.2107728337… USD. The correct cost to be inferred is also the rounded amount of 53.21 USD. We would like a mechanism to allow us to infer the desired precision.

This mechanism cannot unfortunately be solely based on commodity: different accounts may track currencies with different precisions. As a real-world example, I have a retail FOREX trading account that really uses 4 digits of precision for its prices and deposits.

### <a id="precision-of-balance-assertions"></a>Precision of Balance Assertions

The precision of a balance assertions is also subject to this problem, assertions like this one:

    2014-04-01 balance Assets:Investments:Cash   4526.77 USD

The user does not intend for this balance check to precisely sum up to 4526.77000000… USD. However, it this cash account previously received a deposit with a greater precision as in the previous section’s example, then we have a problem. Now the cash amount contains some of the crumbs deposited from the interpolation (0.0067 USD). If we were able to find a good solution for the automatic rounding of postings in the previous section, this would not be a problem. But in the meantime, we must find a solution.

Beancount’s current approach is a kludge: it uses a [<span class="underline">user-configurable tolerance</span>](https://bitbucket.org/blais/beancount/src/f9f90945dd751ecec5d0f63c1bccc372ed21f58f/src/python/beancount/ops/balance.py?at=default#cl-92) of 0.0150 (in any unit). We’d like to change this so that the tolerance used is able to depend on the commodity, the account, or even the particular directive in use.

<a id="other-systems"></a>Other Systems
---------------------------------------

Other command-line accounting systems differ in how they choose that tolerance:

-   Ledger attempts to automatically derive the precision to use for its balance checks by using recently parsed context (in file order). The precision to be used is that of the last value parsed for the particular commodity under consideration. This can be problematic: it can lead to [<span class="underline">unnecessary side-effects between transactions which can be difficult to debug</span>](https://groups.google.com/d/msg/ledger-cli/m-TgILbfrwA/cTHg2juqEJgJ).

-   HLedger, on the other hand, uses global precision settings. [<span class="underline">The whole file is processed first, then the precisions are derived from the most precise numbers seen in the entire input file.</span>](https://groups.google.com/d/msg/ledger-cli/m-TgILbfrwA/SoGZDNhlDOkJ)

-   At the moment, Beancount uses a [<span class="underline">constant value</span>](https://bitbucket.org/blais/beancount/src/c194c7fa6c15a0356e9d26b20b471f0868843c42/src/python/beancount/core/complete.py?at=default#cl-25) for the tolerance used in its [<span class="underline">balance checking algorithm</span>](https://bitbucket.org/blais/beancount/src/c194c7fa6c15a0356e9d26b20b471f0868843c42/src/python/beancount/ops/validation.py?at=default#cl-391) (0.005 of any unit). This is weak and should, at the very least, be commodity-dependent, if not also dependent on the particular account in which the commodity is used.

<a id="proposal"></a>Proposal
-----------------------------

### <a id="automatically-inferring-tolerance"></a>Automatically Inferring Tolerance

Beancount should derive its precision using a method entirely *local* to each transaction, perhaps with a global value for defaults. That is, for each transaction, it will inspect postings with simple amounts (no cost, no price) and infer the precision to be used for tolerance as half of that of the most precise amount entered by the user on this transaction. For example:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       4.278  RGAGX {53.21 USD} 
      Assets:Investments:Cash     -227.6324 USD
      Expenses:Commissions           9.95   USD

The number of digits for the precision to be used here is the maximum of the 2nd and 3rd postings, that is, max(4, 2) = 4. The first postings is ignored because its amount is the result of a mathematical operation. The tolerance value should be *half* of the most precise digit, that is 0.00005 USD. This should allow the user to use an arbitrary precision, simply by inserting more digits in the input.

Only fractional digits will be used to derive precision… an integer should imply exact matching. The user could specify a single trailing period to imply a sub-dollar precision. For example, the following transaction should fail to balance because the calculated amount is 999.999455 USD:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       23.45 RGAGX {42.6439 USD} 
      Assets:Investments:Cash        -1000 USD

Instead, the user should explicitly allow for some tolerance to be used:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       23.45 RGAGX {42.6439 USD} 
      Assets:Investments:Cash       -1000. USD

Or better, use 1000.00 USD. This has the disadvantage that is prevents the user from specifying the simpler integer amount. I’m not sure if this is a big deal.

Finally, no global effect implied by transactions will be applied. No transaction should ever affect any other transaction’s balancing context.

### <a id="inference-on-amounts-held-at-cost"></a>Inference on Amounts Held at Cost

An idea from by Matthew Harris ([<span class="underline">here</span>](https://groups.google.com/d/msg/beancount/5u-xgR-ttjg/sXfU32ItRscJ)) is that we could also use the value of the to the smallest decimal of the number of units times the cost as a number to use in establishing the tolerance for balancing transactions. For example, in the following transaction:

    2014-05-06 * “Buy mutual fund”
      Assets:Investments:RGXGX       23.45 RGAGX {42.6439 USD} 
      ...

The tolerance value that could be derived is

0.01 RGAGX x 42.6439 USD = **0.426439 USD**

The original use case presented by Matthew was of a transaction that did not contain a simple amount, just a conversion with both legs held at cost:

      2011-01-25 * "Transfer of Assets, 3467.90 USD"
        * Assets:RothIRA:Vanguard:VTIVX  250.752 VTIVX {18.35 USD} @ 13.83 USD  
        * Assets:RothIRA:DodgeCox:DODGX  -30.892 DODGX {148.93 USD} @ 112.26 USD

I’ve actually tried to implement this and the resulting tolerances are either unacceptably wide or unacceptably small. **It does not work well in practice so I’ve abandoned the idea.**

### <a id="automated-rounding"></a>Automated Rounding

For values that are automatically calculated, for example, on auto-postings where the remaining value is derived automatically, we should consider rounding the values. No work has been done on this yet; these values are currently not rounded.

### <a id="fixing-balance-assertions"></a>Fixing Balance Assertions

To fix balance assertions, we will derive the required precision by the number of digits used in the balance amount itself, by looking at the most precision fractional digit and using half of that digit’s value to compute the tolerance:

    2014-04-01 balance Assets:Investments:Cash   4526.7702 USD

This balance check implies a precision of 0.00005 USD.

If you use an integer number of units, no tolerance is allowed. The precise number should match:

    2014-04-01 balance Assets:Investments:Cash   4526 USD

If you want to allow for sub-dollar variance, use a single comma:

    2014-04-01 balance Assets:Investments:Cash   4526. USD

This balance check implies a precision of 0.50 USD.

### <a id="approximate-assertions"></a>Approximate Assertions

Another idea, proposed in [<span class="underline">this ticket on Ledger</span>](https://github.com/ledger/ledger/pull/329), proposes an explicitly approximate assertion.

We could implement it this way (just an idea):

    2014-04-01 balance Assets:Investments:Cash   4526.00 +/- 0.05 USD 

<a id="accumulating-reporting-residuals"></a>Accumulating & Reporting Residuals
-------------------------------------------------------------------------------

In order to explicitly render and monitor the amount of rounding errors that occur in a Ledger, we should [<span class="underline">accumulate it to an Equity account</span>](https://groups.google.com/d/msg/ledger-cli/m-TgILbfrwA/YjkmOM3LHXIJ), such as “Equity:Rounding”. This should be turned on optionally. It should be possible for the user to specify an account to be used to accumulate the error. Whenever a transaction does not balance exactly, the residual, or rounding error, will be inserted as a posting of the transaction to the equity account.

By default, this accumulation should be turned off. It’s not clear whether the extra postings will be disruptive yet (if they’re not, maybe this should be turned on by default; practice will inform us).

<a id="implementation"></a>Implementation
-----------------------------------------

The implementation of this proposal is [<span class="underline">documented here</span>](08_precision_tolerances.md).
