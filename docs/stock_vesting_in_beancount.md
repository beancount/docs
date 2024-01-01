# Stock Vesting in Beancount<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca), June 2015

[<u>http://furius.ca/beancount/doc/vesting</u>](http://furius.ca/beancount/doc/vesting)

## Introduction<a id="introduction"></a>

This document explains the vesting of restricted stock units in Beancount, by way of an example. This example may not exactly match your situation, but enough detail is provided that you should be able to adapt it for your own particular differences.

A working example file can be found [<u>here</u>](http://github.com/beancount/beancount/tree/master/examples/vesting/vesting.beancount) to follow along with this text.

## Restricted Stock Compensation<a id="restricted-stock-compensation"></a>

Many technology companies offer their employees incentive compensation in the form of “grants” (or “awards”) of “restricted stock units” (RSU), which is essentially a promise for the “release” to you of actual shares in the future. The stock is “restricted” in the sense that you cannot access it—you only receive it when it “vests”, and this happens based on a schedule. Typically, you are promised a fixed number of shares that vest every quarter or every month over a period of 3 or 4 years. If you leave the company, your remaining unvested shares are lost. <img src="stock_vesting_in_beancount/media/6a910c80cfb0385f9cff8de1b5976716a1eb7324.jpg" style="width:2.18229in;height:1.26744in" />

One way you can view these RSUs is as an asset, a receivable that arrives regularly over time. These RSUs are essentially compensation denominated in the currency of the company’s shares itself. We want to track the unraveling of these unvested units, and correctly account for their conversion to real stock with a cost basis and including whatever taxes were paid upon vesting.

## Tracking Awards<a id="tracking-awards"></a>

### Commodities<a id="commodities"></a>

First we want to define some commodities. In this example, I work for “Hooli Inc.” and will eventually receive shares of that company (valued in US dollars):

    1990-12-02 commodity HOOL
      name: "Common shares of Hooli Inc."
      quote: USD

We will also want to track the amount of unvested shares:

    2013-01-28 commodity HOOL.UNVEST
      name: "Unvested shares of Hooli from awards."

### Accounts for Awards<a id="accounts-for-awards"></a>

Grants received is income. I use “Income:US:Hooli” as the root for all income accounts from Hooli, but in particular, I define an account for the awards, which contains units of unvested stock:

    2013-01-28 open Income:US:Hooli:Awards        HOOL.UNVEST

When the stock vests, we will need to book the other side of this income somewhere, so we define an expenses account to count how much stock has been vested over a period of time:

    2014-01-28 open Expenses:Hooli:Vested         HOOL.UNVEST

### Receiving Awards<a id="receiving-awards"></a>

When you receive a new award (this may occur every year, for example, some people call this a “stock refresh”), you receive it as income and deposit it into a fresh new account, used to track this particular award:

    2014-04-02 * "Award S0012345"
      Income:US:Hooli:Awards                -1680 HOOL.UNVEST
      Assets:US:Hooli:Unvested:S0012345      1680 HOOL.UNVEST

    2014-04-02 open Assets:US:Hooli:Unvested:S0012345

You may have multiple active awards at the same time. It’s nice to have a separate account per award, as it offers a natural way to list their contents and when the award expires, you can close the account—the list of open award accounts gives you the list of outstanding & actively vesting awards. In this example I used the number of the award (#S0012345) as the sub-account name. It’s useful to use the number as the statements typically include it.

I like to keep all the awards in a small dedicated section.

## Vesting Events<a id="vesting-events"></a>

Then I have a different section that contains all the transactions that follow a vesting event.

### Accounts<a id="accounts"></a>

First, when we vest stock, it’s a taxable income event. The cash value for the stock needs an Income account:

    2013-04-04 open Income:US:Hooli:RSU

Taxes paid should be on the annual expenses accounts you should have defined somewhere else to account for that year’s taxes (this is covered elsewhere in the cookbook):

    2015-01-01 open Expenses:Taxes:TY2015:US:StateNY
    2015-01-01 open Expenses:Taxes:TY2015:US:Federal
    2015-01-01 open Expenses:Taxes:TY2015:US:SocSec
    2015-01-01 open Expenses:Taxes:TY2015:US:SDI
    2015-01-01 open Expenses:Taxes:TY2015:US:Medicare
    2015-01-01 open Expenses:Taxes:TY2015:US:CityNYC

After paying taxes on the received income, the remaining cash is deposited in a limbo account before getting converted:

    2013-01-28 open Assets:US:Hooli:RSURefund

Also, in another section we should have an account for the brokerage which holds and manages the shares for you:

    2013-04-04 open Assets:US:Schwab:HOOL

Generally you don’t have a choice for this broker because the company you work normally makes an arrangement with an external firm in order to administer the restricted stock program. Typical firms doing this type of administration are Morgan Stanley, Salomon Smith Barney, Schwab, even E\*Trade. In the example we’ll use a Schwab account.

And we also need some sort of checking account to receive cash in lieu of fractional shares. I’ll assume a Bank of America account in the example:

    2001-01-01 open Assets:US:BofA:Checking

### Vesting<a id="vesting"></a>

First, the vesting events themselves:

    2015-05-27 * "Vesting Event - S0012345 - HOOL" #award-S0012345 ^392f97dd62d0
      doc: "2015-02-13.hooli.38745783.pdf"
      Income:US:Hooli:RSU                    -4597.95 USD
      Expenses:Taxes:TY2015:US:Medicare         66.68 USD
      Expenses:Taxes:TY2015:US:Federal        1149.48 USD
      Expenses:Taxes:TY2015:US:CityNYC         195.42 USD
      Expenses:Taxes:TY2015:US:SDI               0.00 USD
      Expenses:Taxes:TY2015:US:StateNY         442.32 USD
      Expenses:Taxes:TY2015:US:SocSec          285.08 USD
      Assets:US:Hooli:RSURefund               2458.97 USD

This corresponds line-by-line to a payroll stub that I receive each vesting event for each award. Since all the RSU awards at Hooli vest on the same day of the month, this means that I have clusters of these, one for each award (in the example file I show two awards).

Some observations are in order:

-   The value of the Income posting consists of the number of shares vested times the FMV of the stock. In this case, that is 35 shares ⨉ $131.37/share = $4597.95. I just write the dollar amount because it is provided to me on the pay stub.

-   Receiving vested stock is a taxable income event, and Hooli automatically withholds taxes and pays them to the government on its employees’ behalf. These are the Expenses:Taxes accounts corresponding to your W-2.

-   Finally, I don’t directly deposit the converted shares to the brokerage account; this is because the remainder of cash after paying tax expenses is not necessarily a round number of shares. Therefore, I used a limbo account (`Assets:US:Hooli:RSURefund`) and decouple the receipt from the conversion.

This way, each transaction corresponds exactly to one pay stub. It makes it easier to enter the data.

Also note that I used a unique link (`^392f97dd62d0`) to group all the transactions for a particular vesting event. You could also use tags if you prefer.

### Conversion to Actual Stock<a id="conversion-to-actual-stock"></a>

Now we’re ready to convert the remaining cash to stock units. This happens in the brokerage firm and you should see the new shares in your brokerage account. The brokerage will typically issue a “stock release report” statement for each vesting event for each award, with the details necessary to make the conversion, namely, the actual number of shares converted from cash and the cost basis (the FMV on the vesting day):

    2015-05-25 * "Conversion into shares" ^392f97dd62d0
      Assets:US:Schwab:HOOL                   18 HOOL {131.3700 USD}
      Assets:US:Hooli:RSURefund
      Assets:US:Hooli:Unvested:S0012345      -35 HOOL.UNVEST
      Expenses:Hooli:Vested                   35 HOOL.UNVEST

The first two postings deposit the shares and subtract the dollar value from the limbo account where the vesting transaction left the remaining cash. You should make sure to use the specific FMV price provided by the statement and not an approximate price, because this has tax consequences later on. Note that you cannot buy fractional shares, so the cost of the rounded amount of shares (18) will leave some remaining cash in the limbo account.

The last two postings deduct from the balance of unvested shares and I “receive” an expenses; that expenses account basically counts how many shares were vested over a particular time period.

Here again you will probably have one of these conversions for each stock grant you have. I enter them separately, so that one statement matches one transaction. This is a good rule to follow.

### Refund for Fractions<a id="refund-for-fractions"></a>

After all the conversion events have moved cash out of the limbo account, it is left the fractional remainders from all the conversions. In my case, this remainder is refunded by Hooli 3-4 weeks after vesting as a single separate pay stub that includes all the remainders (it even lists each of them separately). I enter this as a transaction as well:

    2015-06-13 * "HOOLI INC       PAYROLL" ^392f97dd62d0
      doc: "2015-02-13.hooli.38745783.pdf"
      Assets:US:Hooli:RSURefund            -94.31 USD
      Assets:US:Hooli:RSURefund             -2.88 USD ; (For second award in example)
      Assets:US:BofA:Checking               97.19 USD

After the fractions have been paid the limbo account should be empty. I verify this claim using a balance assertion:

    2015-06-14 balance Assets:US:Hooli:RSURefund  0 USD

This provides me with some sense that the numbers are right.

### Organizing your Input<a id="organizing-your-input"></a>

I like to put all the vesting events together in my input file; this makes them much easier to update and reconcile, especially with multiple awards. For example, with two awards I would have multiple chunks of transactions like this, separated with 4-5 empty lines to delineate them:

    2015-05-27 * "Vesting Event - S0012345 - HOOL" #award-S0012345 ^392f97dd62d0
      doc: "2015-02-13.hooli.38745783.pdf"
      Income:US:Hooli:RSU                    -4597.95 USD
      Assets:US:Hooli:RSURefund               2458.97 USD
      Expenses:Taxes:TY2015:US:Medicare         66.68 USD
      Expenses:Taxes:TY2015:US:Federal        1149.48 USD
      Expenses:Taxes:TY2015:US:CityNYC         195.42 USD
      Expenses:Taxes:TY2015:US:SDI               0.00 USD
      Expenses:Taxes:TY2015:US:StateNY         442.32 USD
      Expenses:Taxes:TY2015:US:SocSec          285.08 USD

    2015-05-27 * "Vesting Event - C123456 - HOOL" #award-C123456 ^392f97dd62d0
      doc: "2015-02-13.hooli.38745783.pdf"
      Income:US:Hooli:RSU                    -1970.55 USD
      Assets:US:Hooli:RSURefund               1053.84 USD
      Expenses:Taxes:TY2015:US:Medicare         28.58 USD
      Expenses:Taxes:TY2015:US:Federal         492.63 USD
      Expenses:Taxes:TY2015:US:CityNYC          83.75 USD
      Expenses:Taxes:TY2015:US:SDI               0.00 USD
      Expenses:Taxes:TY2015:US:StateNY         189.57 USD
      Expenses:Taxes:TY2015:US:SocSec          122.18 USD

    2015-05-25 * "Conversion into shares" ^392f97dd62d0
      Assets:US:Schwab:HOOL                        18 HOOL {131.3700 USD}
      Assets:US:Hooli:RSURefund
      Assets:US:Hooli:Unvested:S0012345           -35 HOOL.UNVEST
      Expenses:Hooli:Vested                        35 HOOL.UNVEST

    2015-05-25 * "Conversion into shares" ^392f97dd62d0
      Assets:US:Schwab:HOOL                         9 HOOL {131.3700 USD}
      Assets:US:Hooli:RSURefund
      Assets:US:Hooli:Unvested:C123456            -15 HOOL.UNVEST
      Expenses:Hooli:Vested                        15 HOOL.UNVEST

    2015-06-13 * "HOOLI INC       PAYROLL" ^392f97dd62d0
      doc: "2015-02-13.hooli.38745783.pdf"
      Assets:US:Hooli:RSURefund                -94.30 USD
      Assets:US:Hooli:RSURefund                 -2.88 USD
      Assets:US:BofA:Checking                   97.18 USD

    2015-02-14 balance Assets:US:Hooli:RSURefund    0 USD

## Unvested Shares<a id="unvested-shares"></a>

### Asserting Unvested Balances<a id="asserting-unvested-balances"></a>

Finally, you may occasionally want to assert the number of unvested shares. I like to do this semi-annually, for example. The brokerage company that handles the RSUs for Hooli should be able to list how many unvested shares of each award remain, so it’s as simple as looking it up on a website:

    2015-06-04 balance Assets:US:Hooli:Unvested:S0012345  1645 HOOL.UNVEST
    2015-06-04 balance Assets:US:Hooli:Unvested:C123456    705 HOOL.UNVEST

### Pricing Unvested Shares<a id="pricing-unvested-shares"></a>

You can also put a price on the unvested shares in order to estimate the unvested dollar amount. You should use a fictional currency for this, because we want to avoid a situation where a balance sheet is produced that includes these unvested assets as regular dollars:

    2015-06-02 price HOOL.UNVEST               132.4300 USD.UNVEST

At the time of this writing, the bean-web interface does not convert the units if they are not held at cost, but using the SQL query interface or writing a custom script you should be able to produce those numbers:

    $ bean-query examples/vesting/vesting.beancount 

    beancount> select account, sum(convert(position, 'USD.UNVEST')) as unvested 
               where account ~ 'Unvested' group by account;

                 account                     unvested       
    --------------------------------- ----------------------
    Assets:US:Hooli:Unvested:S0012345 217847.3500 USD.UNVEST
    Assets:US:Hooli:Unvested:C123456   93363.1500 USD.UNVEST

## Selling Vested Stock<a id="selling-vested-stock"></a>

After each vesting event, the stock is left in your brokerage account. Selling this stock proceeds just as in any other trading transaction (see [<u>Trading with Beancount</u>](trading_with_beancount.md) for full details). For example, selling the shares from the example would look something like this:

    2015-09-10 * "Selling shares"
      Assets:US:Schwab:HOOL        -26 HOOL {131.3700 USD} @ 138.23 USD
      Assets:US:Schwab:Cash    3593.98 USD
      Income:US:Schwab:Gains

Here you can see why it matters that the cost basis you used on the conversion event is the correct one: You will have to pay taxes on the difference (in `Income:US:Schwab:Gains`). In this example the taxable difference is (138.23 - 131.37) dollars per share.

I like to keep all the brokerage transactions in a separate section of my document, where other transactions related to the brokerage occur, such as fees, dividends and transfers.

## Conclusion<img src="stock_vesting_in_beancount/media/04de27aeb8e7b7cbc9201ce82ae780d21cec36fb.jpg" style="width:2.04688in;height:1.39525in" /><a id="conclusion"></a>

This is a simple example that is modeled after how technology companies deal with this type of compensation. It is by no means comprehensive, and some of the details will necessarily vary in your situation. In particular, it does not explain how to deal with options (ISOs). My hope is that there is enough meat in this document to allow you to extrapolate and adapt to your particular situation. If you get stuck, please reach out on the [<u>mailing-list</u>](http://furius.ca/beancount/doc/mailing-list).
