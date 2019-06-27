Command-line Accounting Cookbook
================================

[<span class="underline">Martin Blais</span>](mailto:blais@furius.ca), July 2014

[<span class="underline">http://furius.ca/beancount/doc/cookbook</span>](http://furius.ca/beancount/doc/cookbook)

> [<span class="underline">Introduction</span>](#introduction)
>
> [<span class="underline">A Note of Caution</span>](#a-note-of-caution)
>
> [<span class="underline">Account Naming Conventions</span>](#account-naming-conventions)
>
> [<span class="underline">Choosing an Account Type</span>](#choosing-an-account-type)
>
> [<span class="underline">Choosing Opening Dates</span>](#choosing-opening-dates)
>
> [<span class="underline">How to Deal with Cash</span>](#how-to-deal-with-cash)
>
> [<span class="underline">Cash Withdrawals</span>](#cash-withdrawals)
>
> [<span class="underline">Tracking Cash Expenses</span>](#tracking-cash-expenses)
>
> [<span class="underline">Salary Income</span>](#salary-income)
>
> [<span class="underline">Employment Income Accounts</span>](#employment-income-accounts)
>
> [<span class="underline">Booking Salary Deposits</span>](#booking-salary-deposits)
>
> [<span class="underline">Vacation Hours</span>](#vacation-hours)
>
> [<span class="underline">401k Contributions</span>](#k-contributions)
>
> [<span class="underline">Vesting Stock Grants</span>](#vesting-stock-grants)
>
> [<span class="underline">Other Benefits</span>](#other-benefits)
>
> [<span class="underline">Points</span>](#points)
>
> [<span class="underline">Food Benefits</span>](#food-benefits)
>
> [<span class="underline">Currency Transfers & Conversions</span>](#currency-transfers-conversions)
>
> [<span class="underline">Investing and Trading</span>](#investing-and-trading)
>
> [<span class="underline">Accounts Setup</span>](#accounts-setup)
>
> [<span class="underline">Funds Transfers</span>](#funds-transfers)
>
> [<span class="underline">Making a Trade</span>](#making-a-trade)
>
> [<span class="underline">Receiving Dividends</span>](#receiving-dividends)
>
> [<span class="underline">Conclusion</span>](#conclusion)

Introduction
------------

The best way to learn the double-entry method is to look at real-world examples. The method is elegant, but it can seem unintuitive to the newcomer how transactions have to be posted in order to perform the various operations that one needs to do in counting for different types financial events. This is why I wrote this cookbook. It is not meant to be a comprehensive description of all the features supported, but rather a set of practical guidelines to help you solve problems. I think this will likely be the most useful document in the Beancount documentation set!

All the examples here apply to any double-entry accounting system: Ledger, GnuCash, or even commercial systems. Some of the details may differ only slightly. This cookbook is written using the syntax and calculation method of the Beancount software. This document also assumes that you are already familiar with the [<span class="underline">general balancing concepts of the double-entry method</span>](http://furius.ca/beancount/doc/intro) and with at least some of the syntax of Beancount which is available from its [<span class="underline">user’s manual</span>](http://furius.ca/beancount/doc/users-manual) or its [<span class="underline">cheat sheet</span>](10_beancount_cheat_sheet.md). If you haven’t begun writing down your first file, you will want to read [<span class="underline">Getting Started with Beancount</span>](05_getting_started_with_beancount.md) and do that first.

Command-line accounting systems are agnostic about the types of things they can count and allow you to get creative with the kinds of units that you can invent to track various kinds of things. For instance, you can count “IRA contribution dollars,” which are not real dollars, but which correspond to “possible contributions in real dollars,” and you obtain accounts of assets, income and expenses types for them - it works. Please do realize that some of those clever tricks may not be possible in more traditional accounting systems. In addition, some of the operations that would normally require a manual process in these systems can be automated away for us, e.g., “closing a year” is entirely done by the software at any point in time, and balance assertions provide a safeguard that allow us to change the details of past transactions with little risk, so there is no need to “reconcile” by baking the past into a frozen state. More flexibility is at hand.

Finally, if you have a transaction entry problem that is not covered in this document, please do leave a comment in the margin, or write up your problem to the [<span class="underline">Ledger mailing-list</span>](https://groups.google.com/forum/#!forum/ledger-cli). I would like for this document to cover as many realistic scenarios as possible.

### A Note of Caution

While reading this, please take note that the author is a dilettante: I am a computer scientist, not an accountant. In fact, apart from a general course I took in college and having completed the first year of a CFA program, I have no real training in accounting. Despite this, I do have some practical experience in maintaining three set of books using this software: my personal ledger (8 years worth of full financial data for all accounts), a joint ledger with my spouse, and the books of a contracting and consulting company I used to own. I also used my double-entry system to communicate with my accountant for many years and he made suggestions. Nevertheless… I may be making fundamental mistakes here and there, and I would appreciate you leaving a comment in the margin if you find anything dubious.

Account Naming Conventions
--------------------------

You can define any account name you like, as long as it begins with one of the five categories: Assets, Liabilities, Income, Expenses, or Equity (note that you can customize those names with options - see the [<span class="underline">Language Syntax document</span>](http://furius.ca/beancount/doc/users-manual) for details). The accounts names are generally defined to have multiple name *components,* separated by a colon (:), which imply an accounts hierarchy, or “[<span class="underline">chart of accounts</span>](http://en.wikipedia.org/wiki/Chart_of_accounts)”:

    Assets:Component1:Component2:Component3:...

Over time, I’ve iterated over many ways of defining my account names and I have converged to the following convention for Assets, Liabilities, and Income accounts:

    Type : Country : Institution : Account : SubAccount

What I like about this is that when you render a balance sheet, the tree that gets rendered nicely displays accounts by country first, then by institution.

Some example account names:

    Assets:US:BofA:Savings       ; Bank of America “Savings” account
    Assets:CA:RBC:Checking       ; Royal Bank of Canada “Checking” account
    Liabilities:US:Amex:Platinum ; American Express Platinum credit card
    Liabilities:CA:RBC:Mortgage  ; Mortgage loan account at RBC
    Income:US:ETrade:Interest    ; Interest payments in E*Trade account
    Income:US:Acme:Salary        ; Salary income from ACME corp.

Sometimes I use a further sub-account or two, when it makes sense. For example, Vanguard internally keeps separate accounts depending on whether the contributions were from the employee or the employer’s matching amount:

    Assets:US:Vanguard:Contrib401k:RGAGX  ; My contributions to this fund
    Assets:US:Vanguard:Match401k:RGAGX    ; Employer contributions

For investment accounts, I tend organize all their contents by storing each particular type of stock in its own sub-account:

    Assets:US:ETrade:Cash        ; The cash contents of the account
    Assets:US:ETrade:FB          ; Shares of Facebook
    Assets:US:ETrade:AAPL        ; Shares of Apple
    Assets:US:ETrade:MSFT        ; Shares of Microsoft
    …

This automatically organizes the balance sheet by types of shares, which I find really nice.

Another convention that I like is to use the same institution component name when I have different related types of accounts. For instance, the E\*Trade assets account above has associated income streams that would be booked under similarly named accounts:

    Income:US:ETrade:Interest    ; Interest income from cash deposits
    Income:US:ETrade:Dividends   ; Dividends received in this account
    Income:US:ETrade:PnL         ; Capital gains or losses from trades
    …

For “Expenses” accounts, I find that there are generally no relevant institutions. For those it makes more sense to treat them as categories and just have a simple hierarchy that corresponds to the kinds of expenses they count, some examples:

    Expenses:Sports:Scuba        ; All matters of diving expenses
    Expenses:Transport:Train     ; Train (mostly Amtrak, but not always)
    Expenses:Transport:Bus       ; Various “chinese bus” companies
    Expenses:Transport:Flights   ; Flights (various airlines)
    … 

I have a *lot* of these, like 250 or more. It is really up to you to decide how many to define and how finely to aggregate or “categorize” your expenses this way. But of course, you should only define them as you need them; don’t bother defining a huge list ahead of time. It’s always easy to add new ones.

It is worth noting that the institution does not have to be a “real” institution. For instance, I owned a condo unit in a building, and I used the Loft4530 “institution” for all its related accounts:

    Assets:CA:Loft4530:Property
    Assets:CA:Loft4530:Association
    Income:CA:Loft4530:Rental
    Expenses:Loft4530:Acquisition:Legal
    Expenses:Loft4530:Acquisition:SaleAgent
    Expenses:Loft4530:Loan-Interest
    Expenses:Loft4530:Electricity
    Expenses:Loft4530:Insurance
    Expenses:Loft4530:Taxes:Municipal
    Expenses:Loft4530:Taxes:School

If you have all of your business in a single country and have no plans to move to another, you might want to skip the country component for brevity.

Finally, for “Equity” accounts, well, …. normally you don’t end up defining many of them, because these are mostly created to report the net income and currency conversions from previous years or the current exercise period on the balance sheet. Typically you will need at least one, and it doesn’t matter much what you name it:

    Equity:Opening-Balances           ; Balances used to open accounts

You can customize the name of the other Equity accounts that get automatically created for the balance sheet.

### Choosing an Account Type

Part of the art of learning what accounts to book transactions to is to come up with relevant account names and design a scheme for how money will flow between those accounts, by jotting down some example transactions. It can get a bit creative. As you’re working out how to “count” all the financial events in your life, you will often end up wondering what account type to select for some of the accounts. Should this be an “Assets” account? Or an “Income” account? After all, other than for creating reports, Beancount doesn’t treat any of these account types differently…

But this does not mean that you can just use any type willy nilly. Whether an account appears in the balance sheet or income statement does matter—there is usually a correct choice. When in doubt, here are some guidelines to choose an account type.

> First, if the amounts to be posted to the account are only relevant to be reported for a *period of time*, they should be one of the income statement accounts: Income or Expenses. On the other hand, if the amount *always* needs to be included in the total balance of an account, then it should be a balance sheet account: Assets or Liabilities.
>
> Second, if the amounts are generally[1] positive, or “good from your perspective,” the account should be either an Assets or an Expenses account. If the amounts are generally negative, or “bad from your perspective,” the account should be either a Liabilities or an Income account.

Based on these two indicators, you should be able to figure out any case. Let’s work through some examples:

-   A restaurant meal represents something that you obtained in exchange for some assets (cash) or a liability (paid by credit card). Nobody ever cares what the “sum total of all food since you were born” amounts to. Only the *transitional* value matters: “How much did I spend in restaurants *this month*?” Or, *since the beginning of the year*? Or, *during this trip?* This clearly points to an Expenses account. But you might wonder… this is a positive number, but it is money I spent? Yes, the account that you spent from was subtracted from (debited) in exchange for the expense you *received*. Think of the numbers in the expenses account as things you received that vanish into the ether right after you receive them. These meals are consumed.. and then they go somewhere. Okay, we’ll stop the analogy here.

-   You own some shares of a bond, and receive an interest payment. This interest is cash deposited in an Assets account, for example, a trading account. What is the other leg to be booked to?

### Choosing Opening Dates

Some of the accounts you need to define don’t correspond to real world accounts. The Expenses:Groceries account represents the sum total of grocery expenses since you started counting. Personally, I like to use my *birth date* on those. There’s a rationale to it: it sums all the groceries you’ve ever spent money on, and this started only when you came to this world.

You can use this rationale on other accounts. For example, all the income accounts associated with an employer should probably be opened at the date you began the job, and end on the date you left. Makes sense.

How to Deal with Cash
---------------------

Let’s start with cash. I typically define two accounts at my birth date:

    1973-04-27 open Assets:Cash
    1973-04-27 open Assets:ForeignCash

The first account is for active use, this represents my wallet, and usually contains only units of my operating currencies, that is, the commodities I usually think of as “cash.” For me, they are USD and CAD commodities.

The second account is meant to hold all the paper bills that I keep stashed in a pocket from trips around the world, so they’re out of the way in some other account and I don’t see them in my cash balance. I transfer those to the main account when I do travel to such places, e.g., if I return to Japan, I’ll move my JPY from Assets:ForeignCash to Assets:Cash right before the trip and use them during that time.

### Cash Withdrawals

An ATM withdrawal from a checking account to cash will typically look like this:

    2014-06-28 * "DDA WITHDRAW 0609C"
      Assets:CA:BofA:Checking                     -700.00 USD
      Assets:Cash

You would see this transaction be imported in your checking account transactions download.

### Tracking Cash Expenses

One mistake people make when you tell them you’re tracking all of your financial accounts is to assume that you have to book every single little irrelevant cash transaction to a notebook. Not so! It is your choice to decide *how many* of these cash transactions to take down (or not).

Personally, I try to minimize the amount of manual effort I put into updating my Ledger. My rule for dealing with cash is this:

> *If it is for food or alcohol, I don’t track it.*
>
> *If it is for something else, I keep the receipt and enter it later.*

This works for me, because the great majority of my cash expenses tend to be food (or maybe I just make it that way by paying for everything else with credit cards). Only a few receipts pile up somewhere on my desk for a couple of months before I bother to type them in.

However, you will need to make occasional adjustments to your cash account to account for these expenses. I don’t actually bother doing this very often… maybe once every three months, when I feel like it. The method I use is to take a snapshot of my wallet (manually, by counting the bills) and enter a corresponding balance assertion:

    2014-05-12 balance Assets:Cash       234.13 USD

Every time I do this I’ll also add a cash distribution adjusted to balance the account:

    2014-06-19 * "Cash distribution"
      Expenses:Food:Restaurant           402.30 USD
      Expenses:Food:Alcohol              100.00 USD
      Assets:Cash                     ; -502.30 USD

    2014-06-20 balance Assets:Cash       194.34 USD

If you wonder why the amounts in the cash account don’t add up (234.13 -502.30 ≠ 194.34), it is because between the two assertions I added to the cash account by doing some ATM withdrawals against the checking account, and those appear somewhere else (in the checking account section). The withdrawal increased the balance of the cash account. It would appear if I rendered a journal for Assets:Cash.

I could have made my life simpler and used a Pad directive if I had booked everything to food—pad entries don’t work solely at the beginning of an account’s history, but also between any two balance assertions on the same account—but I want to book 80% of it to food and 20% alcohol, to more accurately represent my real usage of cash[2].

Finally, if you end up with a long time period between the times that you do this, you may want to “spread out” your expenses by adding more than one cash distribution[3] manually, so that if you generate a monthly report, a large cash expense does not appear as a single lump in or outside that month.

Salary Income
-------------

Accounting for your salary is rewarding: you will be able to obtain a summary of income earned during the year as well as the detail of where the various deductions are going, and you will enjoy the satisfaction of seeing matching numbers from your Beancount reports when you receive your W-2 form from your employer (or on your T4 if you’re located in Canada).

I put all entries related to an employer in their own dedicated section. I start it by setting an event to the date I began working there, for example, using the hypothetical company “Hooli” (from the Silicon Valley show):

    2012-12-13 event "employer" "Hooli Inc."

This allows me to automatically calculate the number of days I’ve been working there. When I leave a job, I’ll change it to the new one, or an empty string, if I don’t leave for another job:

    2019-03-02 event "employer" ""

This section will make several assumptions. The goal is to expose you to the various ideas you can use to account for your income correctly. You will almost certainly end up having to adapt these ideas to your specific situation.

### Employment Income Accounts

Then you define accounts for your pay stubs. You need to make sure that you have an account corresponding to each line of your pay stub. For example, here are some of the income accounts I define for this employment income at Hooli Inc.:

    2012-12-13 open Income:US:Hooli:Salary          USD ; "Regular Pay"
    2012-12-13 open Income:US:Hooli:ReferralBonus   USD ; "Referral bonuses"
    2012-12-13 open Income:US:Hooli:AnnualBonus     USD ; "Annual bonus"
    2012-12-13 open Income:US:Hooli:Match401k       USD ; "Employer 401k match"
    2012-12-13 open Income:US:Hooli:GroupTermLife   USD ; "Group Term Life"

These correspond to regular salary pay, bonuses received for employee referrals, annual bonus, receipts for 401k (Hooli in this example will match some percentage of your contributions to your retirement account), receipts for life insurance (it appears both as an income and an expense), and benefits paid for your gym subscription. There are more, but this is a good example. (In this example I wrote down the names used in the stub as a comment, but you could insert them as metadata instead if you prefer.)

You will need to book taxes withheld at the source to accounts for that year (see the tax section for details on this):

    2014-01-01 open Expenses:Taxes:TY2014:US:Medicare  USD
    2014-01-01 open Expenses:Taxes:TY2014:US:Federal   USD
    2014-01-01 open Expenses:Taxes:TY2014:US:StateNY   USD
    2014-01-01 open Expenses:Taxes:TY2014:US:CityNYC   USD
    2014-01-01 open Expenses:Taxes:TY2014:US:SDI       USD
    2014-01-01 open Expenses:Taxes:TY2014:US:SocSec    USD

These accounts are for Medicare taxes, Federal, New York State and NYC taxes (yes, New York City residents have an additional tax on top of state tax), state disability insurance (SDI) payments, and finally, taxes to pay for social security.

You will also need to have some accounts defined elsewhere for the various expenses that are paid automatically from your pay:

    2012-12-13 open Expenses:Health:Life:GroupTermLife  USD ; "Life Ins."
    2012-12-13 open Expenses:Health:Dental:Insurance    USD ; "Dental"
    2012-12-13 open Expenses:Health:Medical:Insurance   USD ; "Medical"
    2012-12-13 open Expenses:Health:Vision:Insurance    USD ; "Vision"
    2012-12-13 open Expenses:Internet:Reimbursement     USD ; "Internet Reim"
    2012-12-13 open Expenses:Transportation:PreTax      USD ; "Transit PreTax"

These correspond to typical company group plan life insurance payments, premiums for dental, medical and vision insurances, reimbursements for home internet usage, and pre-tax payments for public transit (the city of New York allows you to pay for your MetroCard with pre-tax money through your employer).

### Booking Salary Deposits

Then, when I import details for a payment via direct deposit to my checking account, it will look like this:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking               3364.67 USD

If I haven’t received my pay stub yet, I might book it temporarily to the salary account until I do:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking               3364.67 USD
      ! Income:US:Hooli:Salary

When I receive or fetch my pay stub, I remove this and complete the rest of the postings. A realistic entry for a gross salary of $140,000 would look something like this:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking               3364.67 USD
      Income:US:Hooli:GroupTermLife          -25.38 USD
      Income:US:Hooli:Salary               -5384.62 USD
      Expenses:Health:Dental:Insurance         2.88 USD
      Expenses:Health:Life:GroupTermLife      25.38 USD
      Expenses:Internet:Reimbursement        -34.65 USD
      Expenses:Health:Medical:Insurance       36.33 USD
      Expenses:Transportation:PreTax          56.00 USD
      Expenses:Health:Vision:Insurance         0.69 USD
      Expenses:Taxes:TY2014:US:Medicare       78.08 USD
      Expenses:Taxes:TY2014:US:Federal      1135.91 USD
      Expenses:Taxes:TY2014:US:CityNYC        75.03 USD
      Expenses:Taxes:TY2014:US:SDI             1.20 USD
      Expenses:Taxes:TY2014:US:StateNY       340.06 USD
      Expenses:Taxes:TY2014:US:SocSec        328.42 USD

It’s quite unusual for a salary payment to have no variation at all from its previous one: rounding up or down from the payroll processor will often result in a difference of a penny, social security payments will cap to their maximum, and there are various deductions that will occur from time to time, e.g., deductions on taxable benefits received. Moreover, contributions to a 401k will affect that amounts of taxes withheld at the source. Therefore, you end up having to look at each pay stub individually to enter its information correctly. But this is not as time-consuming as it sounds! Here’s a trick: it’s a lot easier to update your transactions if you list your postings *in the same order as they appear* on your pay stub. You just copy-paste the previous entry, read the pay stub from top to bottom and adjust the numbers accordingly. It takes a minute for each.

It’s worth noting some unusual things about the previous entry. The “group term life” entry has both a $25.38 income leg and an expense one. This is because Hooli pays for the premium (it reads exactly like that on the stubs.) Hooli also reimburses some of home internet, because I use it to deal with production issues. This appears as a *negative* posting to reduce the amount of my expense Expenses:Internet account.

### Vacation Hours

Our pay stubs also include accrued vacation and the total vacation balance, in vacation hours. You can also track these amounts on the same transactions. You need to declare corresponding accounts:

    2012-12-13 open Income:US:Hooli:Vacation           VACHR
    2012-12-13 open Assets:US:Hooli:Vacation           VACHR
    2012-12-13 open Expenses:Vacation:Hooli            VACHR

Vacation that accrues is something you receive and thus is treated as *Income* in units of “VACHR”, and accumulates in an *Assets* account, which holds how many of these hours you currently have available to “spend” as time off. Updating the previous salary income transaction entry:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking               3364.67 USD
      … 
      Assets:US:Hooli:Vacation                 4.62 VACHR
      Income:US:Hooli:Vacation                -4.62 VACHR

4.62 VACHR on a bi-weekly paycheck 26 times per year is 26 x 4.62 ~= 120 hours. At 8 hours per day, that is 15 work days, or 3 weeks, which is a standard vacation package for new US Hooligans in this example.

When you do take time off, you book an expense against your accumulated vacation time:

    2014-06-17 * "Going to the beach today"
      Assets:US:Hooli:Vacation     -8 VACHR
      Expenses:Vacation:Hooli

The *Expenses* account tracks how much vacation you’ve used. From time to time you can check that the balance reported on your pay stub—the amount of vacation left that your employer thinks you have—is the same as that which you have accounted for:

    2014-02-29 balance Assets:US:Hooli:Vacation   112.3400 VACHR

You can “price” your vacation hour units to your hourly rate, so that your vacations *Assets* account shows how much the company would pay you if you decided to quit. Assuming that $140,000/year salary, 40 hour weeks and 50 weeks of work, which is 2000 hours per year, we obtain a rate of $70/hour, which you enter like this:

    2012-12-13 price VACHR  70.00 USD

Similarly, if your vacation hours expires or caps, you can calculate how much dollar-equivalent you’re forfeiting by working too much and giving up your vacation time. You would write off some of the VACHR from your *Assets* account into an income account (representing losses).

### 401k Contributions

The 401k plan allows you to make contributions to a tax-deferred retirement account using pre-tax dollars. This is carried out via withholdings from your pay. To account for those, you simply include a posting with the corresponding contribution towards your retirement account:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking               3364.67 USD
      …
      Assets:US:Vanguard:Cash               1000.00 USD
      … 

If you’re accounting for your available contributions (see the tax section of this document), you will want to reduce your “401k contribution” *Assets* account at the same time. You would add two more postings to the transaction:

    2014-02-28 * "HOOLI INC       PAYROLL"
      Assets:US:BofA:Checking                       3364.67 USD
      …
      Assets:US:Vanguard:Cash                       1000.00 USD
      Assets:US:Federal:PreTax401k                 -1000.00 US401K
      Expenses:Taxes:TY2014:US:Federal:PreTax401k   1000.00 US401K
      … 

If your employer matches your contributions, this may not show on your pay stubs. Because these contributions are not taxable—they are deposited directly to a tax-deferred account—your employer does not have to include them in the withholding statement. You will see them appear directly in your investment account as deposits. You can book them like this to the retirement account’s tax balance:

    2013-03-16 * "BUYMF - MATCH"
      Income:US:Hooli:Match401k           -1173.08 USD
      Assets:US:Vanguard:Cash              1173.08 USD

And then insert a second transaction when you invest this case, or directly purchasing assets from the contribution if you have specified an asset allocation and this is automated by the broker:

    2013-03-16 * "BUYMF - MATCH"
      Income:US:Hooli:Match401k    -1173.08 USD
      Assets:US:Vanguard:VMBPX       106.741 VMBPX {10.99 USD}

Note that the fund that manages your 401k accounts may be tracking your contributions and your employer’s contributions in separate buckets. You would declare sub-accounts for this and make the corresponding changes:

    2012-12-13 open Assets:US:Vanguard:PreTax401k:VMBPX  VMBPX
    2012-12-13 open Assets:US:Vanguard:Match401k:VMBPX   VMBPX

It is common for them to do this in order to track each source of contribution separately, because there are several constraints on rollovers to other accounts that depend on it.

### Vesting Stock Grants

See the [<span class="underline">dedicated document</span>](20_stock_vesting_in_beancount.md) on this topic for more details.

### Other Benefits

You can go crazy with tracking benefits if you want. Here are a few wild ideas.

#### Points

If your employer offers a sponsored massage therapy program on-site, you could presumably book a massage out of your paycheck or even from some internal website (if the company is modern), and you could pay for them using some sort of internal points system, say, “Hooli points”. You could track those using a made-up currency, e.g., “MASSA’s” and which could be priced at 0.50 USD, the price at which you could purchase them:

    2012-12-13 open Assets:US:Hooli:Massage    MASSA
    2012-12-13 price MASSA  0.50 USD

When I purchase new massage points, I

    2013-03-15 * "Buying points for future massages"
      Liabilities:US:BofA:CreditCard    -45.00 USD
      Assets:US:Hooli:Massage              90 MASSA {0.50 USD}

If you’re occasionally awarded some of these points, and you can track that in an Income account.

#### Food Benefits

Like many of the larger technology companies, Hooli presumably provides free food for its employees. This saves time and encourages people to eat healthy. This is a bit of a trend in the tech world right now. This benefit does not show up anywhere, but if you want to price it as part of your compensation package, you can track it using an *Income* account:

    2012-12-13 open Income:US:Hooli:Food

Depending on how often you end up eating at work, you could guesstimate some monthly allowance per month:

    2013-06-30 * "Distribution for food eaten at Hooli"
      Income:US:Hooli:Food		-350 USD
      Expenses:Food:Restaurant

Currency Transfers & Conversions
--------------------------------

If you convert between currencies, such as when performing an international transfer between banks, you need to provide the exchange rate to Beancount. It looks like this:

    2014-03-03 * "Transfer from Swiss account"
      Assets:CH:UBS:Checking       -9000.00 CHF
      Assets:US:BofA:Checking      10000.00 USD @ 0.90 CHF

The balance amount of the second posting is calculated as 10,000.00 USD x 0.90 CHF/USD = 9,000 CHF, and the transaction balances. Depending on your preference, you could have placed the rate on the other posting, like this:

    2014-03-03 * "Transfer from Swiss account"
      Assets:CH:UBS:Checking       -9000.00 CHF @ 1.11111 USD
      Assets:US:BofA:Checking      10000.00 USD

The balance amount of the first posting is calculated as -9000.00 CHF x 1.11111 USD/CHF = 10000.00 USD[4]. Typically I will choose the rate that was reported to me and put it on the corresponding side. You may also want to use the direction that F/X markets use for trading the rate, for example, the Swiss franc trades as USD/CHF, so I would prefer the first transaction. The price database converts the rates in both directions, so it is not that important[5].

If you use wire transfers, which is typical for this type of money transfer, you might incur a fee:

    2014-03-03 * "Transfer from Swiss account"
      Assets:CH:UBS:Checking       -9025.00 CHF
      Assets:US:BofA:Checking      10000.00 USD @ 0.90 CHF
      Expenses:Fees:Wires             25.00 CHF

If you convert cash at one of these shady-looking currency exchange parlors found in tourist locations, it might look like this:

    2014-03-03 * "Changed some cash at the airport in Lausanne"
      Assets:Cash             -400.00 USD @ 0.90 CHF
      Assets:Cash              355.00 CHF
      Expenses:Fees:Services     5.00 CHF

In any case, you should *never* convert currency units using the cost basis syntax, because the original conversion rate needs to be forgotten after depositing the units, and not kept around attached to simple currency. For example, this would be incorrect usage:

    2014-03-03 * "Transfer from Swiss account"
      Assets:CH:UBS:Checking       -9000.00 CHF
      Assets:US:BofA:Checking      10000.00 USD {0.90 CHF}  ; <-bad!

If you did that by mistake, you would incur errors when you attempted to use the newly USD deposited: Beancount would require that you specify the cost of these “USD” in CHF, e.g., “debit from my USD that I changed at 0.90 USD/CHF”. Nobody does this in the real world, and neither should you when you represent your transactions: *once the money has converted, it’s just money in a different currency, with no associated cost.*

Finally, a rather subtle problem is that using these price conversions back and forth at different rates over time breaks the accounting equation to some extent: changes in exchange rate may create small amounts of money out of thin air and all the balances don’t end up summing up to zero. However, this is not a problem, because Beancount implements an elegant solution to automatically correct for this problem, so you can use these conversions freely without having to worry about this: it inserts a special conversions entry on the balance sheet to invert the cumulative effect of conversions for the report and obtain a clean balance of zero. (A discussion of the conversions problem is beyond the scope of this cookbook; please refer to [<span class="underline">Solving the Conversions Problem</span>](http://furius.ca/beancount/doc/conversions) if you’d like to know more.)

Investing and Trading
---------------------

Tracking trades and associated gains is a fairly involved topic. You will find a more complete introduction to profit and loss and a detailed discussion of various scenarios in the [<span class="underline">Trading with Beancount</span>](19_trading_with_beancount.md) document, which is dedicated to this topic. Here we will discuss how to setup your account and provide simple example transactions to get you started.

### Accounts Setup

You should create an account prefix to root various sub-accounts associated with your investment account. Say you have an account at ETrade, this could be “Assets:US:ETrade”. Choose an appropriate institution name.

Your investment account will have a cash component. You should create a dedicated sub-account will represent uninvested cash deposits:

    2013-02-01 open Assets:US:ETrade:Cash     USD

I recommend that you further define a sub-account for each of the commodity types that you will invest in. Although this is not strictly necessary—Beancount accounts may contain any number of commodities—it is a nice way to aggregate all the positions in that commodity together for reporting. Say you will buy shares of LQD and BND, two popular bond ETFs:

    2013-02-01 open Assets:US:ETrade:LQD      LQD
    2013-02-01 open Assets:US:ETrade:BND      BND

This also helps produce nicer reports: balances are often shown at cost and it’s nice to see the total cost aggregated by commodity for various reasons (i.e., each commodity provides exposure to different market characteristics). Using a dedicated sub-account for each commodity held within an institution is a good way to do that. Unless you have specific reasons not to do so, I highly suggest sticking with this by default (you can always change it later by renaming accounts).

Specifying commodity constraints on your accounts will help you detect data entry mistakes. Stock trades tend to be a bit more involved than regular transactions, and this is certainly going to be helpful.

Then, you will hopefully receive income in this account, in two forms: capital gains, or “P&L”, and dividends. I like to account for these by institution, because this is how they have to be declared for taxes. You may also receive interest income. Define these:

    2013-02-01 open Income:US:ETrade:PnL          USD
    2013-02-01 open Income:US:ETrade:Dividends    USD
    2013-02-01 open Income:US:ETrade:Interest     USD

Finally, to account for transaction fees and commissions, you will need some general accounts to receive these:

    1973-04-27 open Expenses:Financial:Fees
    1973-04-27 open Expenses:Financial:Commissions

### Funds Transfers

You will normally add some initial money in this account by making a transfer from an external account, say, a checking account:

    2014-02-04 * "Transferring money for investing"
      Assets:US:BofA:Checking        -2000.00 USD
      Assets:US:ETrade:Cash           2000.00 USD

### Making a Trade

Buying stock should have a posting that deposits the new commodity in the commodity’s sub-account, and debits the cash account to the corresponding amounts plus commissions:

    2014-02-16 * "Buying some LQD"
      Assets:US:ETrade:LQD                 10 LQD {119.24 USD}
      Assets:US:ETrade:Cash          -1199.35 USD
      Expenses:Financial:Commissions     6.95 USD

Note that when you’re buying units of a commodity, you are establishing a new trade lot in the account’s inventory and it is necessary that you provide the cost of each unit (in this example, 119.24 USD per share of LQD). This allows us to account for capital gains correctly.

Selling some of the same stock work similarly, except that an extra posting is added to absorb the capital gain or loss:

    2014-02-16 * "Selling some LQD"
      Assets:US:ETrade:LQD                 -5 LQD {119.24 USD} @ 123.40 USD
      Assets:US:ETrade:Cash            610.05 USD
      Expenses:Financial:Commissions     6.95 USD
      Income:US:Etrade:PnL

Note that the postings of shares removed from the Assets:US:ETrade:LQD account is a lot *reduction* and you must provide information to identify which lot you’re reducing, in this case, by providing the per-share cost basis of 119.24 USD.

I normally let Beancount calculate the capital gain or loss for me, which is why I don’t specify it in the last posting. Beancount will automatically balance the transaction by setting the amount of this posting to -20.80 USD, which is a *gain* of 20.80 USD (remember that the signs are inverted for income accounts). Specifying the sale price of 123.40 USD is optional, and it is *ignored* for the purpose of balancing the transaction, the cash deposit and commissions legs determine the profit.

### Receiving Dividends

Receiving dividends takes on two forms. First, you can receive dividends in cash, which will go into the cash account:

    2014-02-16 * "Dividends from LQD"
      Income:US:ETrade:Dividends      -87.45 USD
      Assets:US:ETrade:Cash            87.45 USD

Note that the source of the dividends isn’t specified here. You could use a sub-account of the income account to count it separately.

Or you can receive dividends in shares reinvested:

    2014-06-27 * "Dividends reinvested"
      Assets:US:Vanguard:VBMPX      1.77400 VBMPX {10.83 USD}
      Income:US:Vanguard:Dividends   -19.21 USD

This is booked similarly to a stock purchase, and you also have to provide the cost basis of the received units. This would typically happen in a non-taxable retirement account.

Refer to the [<span class="underline">Trading with Beancount</span>](19_trading_with_beancount.md) document for a more thorough discussion and numerous and more complex examples.

### Choosing a Date

Buying or selling a single lot of stock typically involves multiple events over time: the trade is placed, the trade is filled (usually on the same day), the trade is settled. Settlement usually occurs 2 or 3 business days after the trade is filled.

For simplicity, I recommend using the trade date as the date of your transaction. In the US, this is the date that is recognized for tax purposes, and settlement has no impact on your account (brokers typically won’t allow you to trade without the corresponding cash or margin anyhow). So normally I don’t bother creating separate entries for settlement, it’s not very useful.

More complex schemes can be envisioned, e.g. you could store the settlement date as a metadata field and then use it in scripts later on, but that’s beyond the scope of this document.

Conclusion
----------

This document is incomplete. I have many more example use cases that I’m planning to add here as I complete them. I will be announcing those on the mailing-list as they materialize. In particular, the following topics will be discussed:

-   Health Care Expenses, e.g., insurance premiums and rebates

-   Taxes

-   IRAs, 401k and other tax-deferred accounts

-   Real Estate

-   Options

[1] This is not strictly always true: in accounting for companies, some account types are held at their opposite value for reasons, usually to offset the value of another account of the same type. These are called “contra” accounts. But as an individual, you’re quite unlikely to have one of those. If you’re setting up a chart of accounts for a company, Beancount doesn’t actually care whether the balance is of one sign or other. You declare contra-accounts just like regular accounts.

[2] I am considering supporting an extended version of the Pad directive that can take a percentage value and make it possible to pad only a percentage of the full amount, to automate this.

[3] Yet another extension to Beancount involves support multiple Pad directives between two balance assertions and automatically support this spreading out of padding directives.

[4] If you’re concerned about the issue of precision or rounding in balancing, see [<span class="underline">this document</span>](http://furius.ca/beancount/doc/rounding).

[5] Note that if the price database needs to invert the date its calculation may result in a price with a large number of digits. Beancount uses IEEE decimal objects and the default context of the Python implementation is 28 digits, so inverting 0.9 will result in 1.111111….111 with 28 digits.
