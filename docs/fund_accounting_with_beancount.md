Fund Accounting with Beancount<a id="title"></a>
================================================

[<span class="underline">Martin Blais</span>](http://plus.google.com/+MartinBlais), Carl Hauser, August 2014

[<span class="underline">http://furius.ca/beancount/doc/proposal-funds</span>](http://furius.ca/beancount/doc/proposal-funds)

*A discussion about how to carry out fund accounting within Beancount, various approaches, solutions and possible extensions.*

Motivation<a id="motivation"></a>
---------------------------------

Multiple users are attempting to solve the problem of fund accounting using command-line accounting systems, partially because this type of accounting occurs in the context of non-profit organizations that have small budgets and would prefer to use free software, and partially because the flexibility and customization required appear to be a good fit for command-line bookkeeping systems.

What is Fund Accounting?<a id="what-is-fund-accounting"></a>
------------------------------------------------------------

For example, see [<span class="underline">this thread</span>](https://groups.google.com/d/msg/ledger-cli/N8Slh2t45K0/nu1ZACCueQYJ):

> *“Another religious duty I compute is effectively tithing (we call it Huqúqu'lláh, and it's computed differently, but that's another story). In order to compute the tithe owed, I accrue 19% of every deposit to a virtual account, and then subtract from that account 19% of every needful expenditure.*
>
> *The total remaining at the end of the year is what I owe in tithe. This tithing account is not a real account, as it exists in no financial institution; but it is real enough as a personal duty. By using virtual account, I can track this "side-band" Liability, and then pay it off from an assets account when the time comes. If I report with --real I will simply see how much I've paid to this Liability; and if I report without --real I see how much Huqúqu'lláh is presently owed.”*
>
> *— John Wiegley*

Here’s another description, as a comment from another user:

> *\[...\] basically the idea that you split your financial life into separate pots called "funds". Each fund has its own chart of accounts (to a certain extent) and each fund obeys Assets+Liabilities+Equities == 0. This is often needed in non-profits where money given for specific purposes has to be accounted separately. The one area of non-separation is that actual asset accounts (e.g. bank accounts) and actual liability accounts (credit cards) may hold or owe money on behalf of multiple funds, so you can't use entirely separate ledger files. At our church we use a program called PowerChurchPlus for this and it works really well. My wife is now treasurer for a community music organization and facing the same problem but on such a small scale that the cost of a commercial program isn't warranted.*
>
> *I've seen what was posted in the ledger-cli list about non-profit accounting using C++ ledger and it just looks like it requires way too much discipline to use the tags correctly and consistently. The fund idea is much easier to explain and use (and the balance account invariant naturally enforced). So I was looking at the Beancount code to see whether I could adapt it to support fund accounting. I think the answer is "yes and relatively easily so". Furthermore, I think this idea has uses even for individuals: a couple of scenarios present themselves. First, I live in a community property state. My wife and I are each likely to inherit property which will be ours individually, but we also have the community property. These can each be treated as a separate fund and we will be able to report on them separately but also together for understanding our overall financial situation. Similarly, it potentially makes sense to account for retirement money with a separate fund for each person.*
>
> *— Carl Hauser*

From the PowerChurchPlus 11.5 Manual (PowerChurch, Inc. 2013):

> *“In accounting, the term fund has a very specific meaning. An Accounting Fund is a self-balancing Chart of Accounts. \[...\] In accounting we need to think of a fund as a division, or sub-group of your church. Each Accounting Fund has its own assets, liabilities, equity, income, transfer and expense accounts.*
>
> *So when would you use an additional fund? If you have an area of your church that needs to produce its own reporting, you would need to use an additional fund. For example, if your church operates a preschool or play school, you might want to set up an additional fund to keep their finances separate from the church's. Depending on your needs, you might want to setup a separate fund for the men's or women's group. You might even setup a new fund to keep track of all fixed assets separately from the daily operating accounts.”*

This is an interesting and apparently common problem. We will describe use cases in the rest of this section.

### Joint Account Management<a id="joint-account-management"></a>

I have personally used this “fund accounting” idea to manage a joint account that I had with my ex-wife, where we would both hold individual accounts—we were both working professionals— and chip in to the joint account as needed. This section describes how I did this[^1].

The accounting for the joint account was held in a separate file. Two sub-accounts were created to hold each of our “portions”:

    2010-01-01 open Assets:BofA:Joint         
    2010-01-01 open Assets:BofA:Joint:Martin  
    2010-01-01 open Assets:BofA:Joint:Judie   

Transfers to the joint account were directly booked into one of the two sub-account:

    2012-09-07 * "Online Xfer Transfer from CK 345"
      Assets:BofA:Joint:Judie          1000.00 USD
      Income:Contributions:Judie

When we would incur expenses, we would reduce the asset account with two legs, one for each subaccount. We often booked them 2:1 to account for difference in income, or I just booked many of the transactions to myself (the fact that it was precisely accounted for does not imply that we weren’t being generous to each other in that way):

    2013-04-27 * "Urban Vets for Grumpy"
      Expenses:Medical:Cat           100.00 USD
      Assets:BofA:Joint:Martin          -50 USD
      Assets:BofA:Joint:Judie           -50 USD

    2013-05-30 * "Takahachi"  "Dinner"
      Expenses:Food:Restaurant        65.80 USD
      Assets:BofA:Joint:Judie        -25.00 USD
      Assets:BofA:Joint:Martin

It was convenient to elide one of the two amounts, as we weren’t being very precise about this.

### Handling Multiple Funds<a id="handling-multiple-funds"></a>

*(Contributed from Carl Hauser)*

Here’s the model used in the PowerChurchPlus system that is mentioned above (replacing the account numbers it uses with Beancount-style names). “Fund” names are *prefixed* to the account names.

    Operations:Assets:Bank:...
    Endowment:Assets:Bank:...
    Operations:Liabilities:CreditCard:...
    Endowment:Liabilities:CreditCard:...
    Operations:Income:Pledges:2014
    Operations:Expenses:Salaries:...
    Operations:Expenses:BuildingImprovement:...
    Endowment:Income:Investments:...
    Endowment:Expenses:BuildingImprovement:...
    …

It is required that any transaction be balanced in every fund that it uses. For example, our Endowment fund often helps pay for things that are beyond the reach of current donations income.

    2014-07-25 * "Bill’s Audio" "Sound system upgrade"
       Endowment:Assets:Bank1:Checking        800.00 USD
       Operations:Assets:Bank1:Checking       200.00 USD
       Endowment:Expenses:BuildingImprovement:Sound -800.00 USD
       Operations:Expenses:BuildingImprovement:Sound -200.00 USD

This represents a single check to Bill’s Audio paid from assets of both the Endowment and Operations funds that are kept in the single external assets account `Assets:Bank1:Checking.`

**Note 1:** An empty fund name could be allowed and the following “:” omitted, and in fact could be the default for people who don’t want to use these features. (i.e., nothing changes if you don’t use these features.) The Fund with the empty string for its name is, of course, distinct from all other Funds.

**Note 2:** `balance` and `pad` directives are not very useful with accounts that participate in more than one Fund. Their use would require knowing the allocation of the account between the different funds and account statements from external holders (banks, e.g.) will not have this information. It might be useful to allow something like

    2014-07-31 balance *:Assets:Bank1:Checking     579.39 USD

as a check that things were right, but automatically correcting it with `pad` entries seems impossible.

A balance sheet report can be run on any Fund *or any combination of Funds* and it will balance. You can keep track of what is owned for each different purpose easily. Transfers between funds are booked as expenses and decreases in the assets of one fund and income and increases in assets of the other. The income and expense accounts used for transfers may be generic (`Operations:Income:Transfer`) or you can use accounts set up for a particular kind of income or expense (`Endowment:Expense:BuildingImprovement:Sound`) would be fine as one leg of a transfer transaction.

The account name syntax here is just one way it might work and relies on Beancount’s use of five specifically-named top-level accounts. Anything to the left of the first of those could be treated as a fund name, or a different separator could be used between the fund part and the account name part. Similarly, I’ve only shown single-level fund names but they might be hierarchical as well. I’m not sure of the value of that, but observe that if transactions balance at the leaf-level funds they will also balance for funds higher in the hierarchy and there might be some mileage there.

For John W.’s *Huqúqu'lláh* example one might set up a Fund whose liabilities were “moral obligations” rather than legal ones (that seems to be the objection to simply tracking the tithes in an ordinary liability account). As income comes in (say, direct deposited in a real bank checking account), book 19% of it to the “moral obligation” fund’s checking account with a matching liability. When needful expenses are made, take back 19% from the “moral obligation” fund’s checking account and reduce the liability. No virtual postings or transactions -- everything must balance. This would work well if for example we were to have a `HisRetirement` fund and a `HerRetirement` fund -- useful to have separate for estate planning purposes -- but more commonly we want to know about our combined retirement which could be defined to be a *virtual* fund `OurRetirement` equal to the sum of `HisRetirement` and `HerRetirement`. Note that this only matters when creating reports: there is no need to do anything except normal, double-entry booking with balanced transactions in each *real* fund. When I say the “sum” of two funds I mean a combination of taking the union of the contained account names, after stripping off the fund names, then summing the balances of the common accounts and keeping the balances of the others.

*(Balance Sheet)* For reporting, one wants the capability for balance by fund and balance summed over a set of funds. I also use a report that shows a subset of funds, one per column, with corresponding account names lined up horizontally and a column at the right that is the “sum”. When all funds are included in this latter report you get a complete picture of what you own and owe and what is set aside for different purposes, or restricted in different ways. Here’s a small sample of a balance sheet for a subset of the church Funds. The terminology is a little different: what Beancount calls Equity is here Net Assets. And because using large numbers of Funds in PowerChurchPlus is not so easy, the NetAssets are actually categorized for different purposes -- this is where I think the ideas we’re exploring here can really shine: if Funds are really easy to create and combine for reporting then some of the mechanisms that PCP has for divvying up assets within a fund become unnecessary. <img src="fund_accounting_with_beancount/media/8c56573ed54aa0aff877dee48727a6f485015884.jpg" style="width:6.5in;height:3.76389in" alt="samplebalsheet.jpg" />

*(Income Statement)* For the Income and Expense report, usually I only care about expenses in one Fund at a time, but adding two funds together makes perfect sense if that’s what you need to do.

For me, this approach to fund accounting is appealing because it relies on and preserves the fundamental principles of double-entry bookkeeping: when transactions sum to 0 the balance sheet equation is always true. Out of this we automatically get the ability to combine *any set of funds* (we don’t have to do anything special when entering transactions or organizing the deep structure of the accounts) and have it make at least arithmetical sense, and we don’t rely on any “magic” associated with renaming or tagging. I don’t see how this can be so easily or neatly achieved by pushing the idea of the “funds” down into the account hierarchy: funds belong *above* the five root accounts (Assets, Liabilities, Equity, Income and Expenses), not below them.

Ideas for Implementation<a id="ideas-for-implementation"></a>
-------------------------------------------------------------

***Some random ideas for now. This needs a bit more work.***

-   If multiple redundant postings are required, the generation of these can be **automated using a [<span class="underline">plugin</span>](beancount_scripting_plugins.md)**. For instance, if a technique similar to [<span class="underline">mirror accounting</span>](http://furius.ca/beancount/doc/mirror) is used in order to “send the same dollars to multiple accounts”, at least the user should not have to do this manually, which would be both tedious and prone to errors.

-   A procedure to **rename accounts** upon parsing could be used, in order to merge multiple files into one. (Allowing the user to install such a mapping is an idea I’ve had for a while but never implemented, though it could be implemented by a plugin filter.)

-   We can rely on the fact that the transactions of **subaccounts may be joined and summed in a parent account** (despite the fact that reporting is lagging behind in that matter at the moment. It will be implemented eventually).

-   Building off the earlier remark about doing something similar to the tag stack for Funds. What if the current tag architecture were extended to allow tags to have a value, `#fund=Operations,` or `#fund=Endowment`. Call them value-tags. You would also need to allow postings to have tags. Semantics of value-tags would be that they could only occur once for any posting, that a tag explicitly on a posting overrides the value-tag inherited from the transaction, and that an explicit tag on a transaction overrides a value from the tag-stack, and that only the last value-tag (with a particular key) in the tag-stack is applied to a transaction. This makes Funds a little less first-class than the earlier proposal to stick them in front of account names, but gets around the minor parsing difficulty previously mentioned. It suggests that opening of accounts within funds is not necessary where the previous syntax suggests that it is. The strict balancing rule for each fund in a transaction can still be implemented as a plugin. And reporting for a fund (or sum of funds) looks like:

    -   select transactions with any posting matching the desired fund (or funds)

    -   collect (and sum if necessary in the obvious way) postings associated with the fund (or funds) being reported on (A)

    -   collect (and sum in the obvious way) postings from the selected transactions not associated with the desired fund (B)

    -   Format a report with (A) as the information for the desired fund or funds and (B) as OTHER. OTHER is needed to make sure that the report balances, but could be omitted by choice.

<!-- -->

    From an implementation perspective this seems more orthogonal to the current status quo, requiring even less change to existing code. It adds a new feature -- value tags and that can then be used by plugins and new reports to do what we want for fund accounting.

Examples<a id="examples"></a>
-----------------------------

*(Carl)* Here is an example of how I might try to handle things associated with my paycheck, which involves deferred compensation (403(b) -- extremely similar to a 401(k)) and a Flexible Spending Account (somewhat similar to an HSA which has been discussed previously on the ledger-cli group).

### Without Funds<a id="without-funds"></a>

(Carl) First, without Funds (this passes a bean-check):

This is how I might set up my pay stub with health insurance, an FSA and 403b contributions in the absence of Funds. One problem is that it distributes Gross Income directly into the 403b and FSA accounts even though it recognizes that the health insurance contribution is a reduction in salary which the 403b and FSA ought to be as well. So tracking contributions to both of those is made more difficult as well as tracking taxable income.

By thinking hard we could fix this -- we would come up with Income and Expense type accounts to represent the contributions, but they would end up looking kind of silly (in my opinion) because they are entirely internal to the accounts system.

See the next example for how it would look using Funds. If you stick out your tongue, rub your tummy and stand on your head you will see that the Funds-based solution is equivalent to what we would have come up with in the paragraph above in terms of the complexity of its transactions -- just as many lines are required. The advantage is primarily a mental one -- it is much easier to see what to do to be both consistent and useful.

    option “title” “Paystub - no funds”

    2014-07-15 open Assets:Bank:Checking
    2014-07-15 open Assets:CreditUnion:Saving
    2014-07-15 open Assets:FedIncTaxDeposits
    2014-07-15 open Assets:Deferred:R-403b
    2014-07-15 open Expenses:OASI
    2014-07-15 open Expenses:Medicare
    2014-07-15 open Expenses:MedicalAid
    2014-07-15 open Expenses:SalReduction:HealthInsurance
    2014-07-15 open Income:Gross:Emp1
    2014-07-15 open Income:EmplContrib:Emp1:Retirement
    2014-01-01 open Assets:FSA

    ; This way of setting up an FSA looks pretty good. It recognizes the
    ; rule that the designated amount for the year is immediately available
    ; (in the Asset account), and that we are obliged to make contributions
    ; to fund it over the course of the year (the Liability account).
    2014-01-01 open Liabilities:FSA
    2014-01-01 ! "Set up FSA for 2014"
      Assets:FSA                                                 	2000 USD
      Liabilities:FSA                                           	-2000 USD

    2014-07-15 ! "Emp1 Paystub"
      Income:Gross:Emp1                                         	-6000 USD
      Assets:Bank:Checking                                       	3000 USD
      Assets:CreditUnion:Saving                                  	1000 USD
      Assets:FedIncTaxDeposits                                    	750 USD
      Expenses:OASI                                               	375 USD
      Expenses:Medicare                                           	100 USD
      Expenses:MedicalAid                                          	10 USD
      Assets:Deferred:R-403b                                      	600 USD
      Liabilities:FSA                                              	75 USD
      Expenses:SalReduction:HealthInsurance                        	90 USD
      Income:EmplContrib:Emp1:Retirement                         	-600 USD
      Assets:Deferred:R-403b

    2014-01-01 open Expenses:Medical
    2014-07-20 ! "Direct expense from FSA"
      Expenses:Medical                                             	25 USD
      Assets:FSA

    2014-07-20 ! "Medical expense from checking"
      Expenses:Medical                                             	25 USD
      Assets:Bank:Checking

    2014-07-20 ! "Medical expense reimbursed from FSA"
      Assets:Bank:Checking                                         	25 USD
      Assets:FSA

### Using Funds<a id="using-funds"></a>

(Carl) And now using Funds (uses proposed features and hence can’t be checked by bean-check):

This is how I might set up my pay stub with health insurance, an FSA and 403b contributions using Funds. I can straightforwardly arrange things so that contributions to the FSA and 403b are recognized as salary reductions for income tax purposes. And I can easily see how much I have contributed to the 403b and how much my employer has contributed.

See the previous example for how it would look without using Funds and which is not as accurate.

What this does NOT do is track taxes ultimately owed on the 403b money. I think that is a matter of one's decision about whether to do cash-basis or accrual-basis accounting. If cash basis those taxes are not a current liability and cannot be reported as such. If accrual basis, they are a current liability and need to be recorded as such when the income is booked.

For cash-basis books, we'd want the ability to report the state of affairs as if taxes were owed, but that is a matter for reporting rather than booking. We need to make sure we have enough identifiable information to automate creating those reports. I believe that taking a Fund-based accounting perspective easily does this.

A problem not solved: what if your basis is different for Federal and State purposes, or even for Federal and multiple different states. Yikes!

I've used the convention that the Fund name precedes the root account name. Note that with appropriate standing on one's head along with pivoting rules you can put the Fund name anywhere. Putting it first emphasizes that it identifies a set of accounts that must balance, and it makes it easy for the txn processor to guarantee this property. Accounts without a fund name in front belong to the Fund whose name is the empty string.


    option "title" "Paystub - no Funds"

    2014-07-15 open Assets:Bank:Checking
    2014-07-15 open Assets:CreditUnion:Saving
    2014-07-15 open Assets:FedIncTaxDeposits
    2014-07-15 open Expenses:OASI
    2014-07-15 open Expenses:Medicare
    2014-07-15 open Expenses:MedicalAid
    2014-07-15 open Expenses:SalReduction:HealthInsurance
    2014-07-15 open Expenses:SalReduction:FSA
    2014-07-15 open Expenses:SalReduction:R-403b
    2014-07-15 open Income:Gross:Emp1
    2014-07-15 open Income:EmplContrib:Emp1:Retirement
    2014-01-01 open FSA:Assets                    	; FSA fund accounts
    2014-01-01 open FSA:Income:Contributions
    2014-01-01 open FSA:Expenses:Medical
    2014-01-01 open FSA:Expenses:ReimburseMedical
    2014-01-01 open FSA:Liabilities
    2014-07-15 open Retirement403b:Assets:CREF    	; Retirement fund accounts
    2014-07-15 open Retirement403b:Income:EmployeeContrib
    2014-07-15 open Retirement403b:Income:EmployerContrib
    2014-07-15 open Retirement403b:Income:EarningsGainsAndLosses

    ; This implements the same idea as above for the FSA, of balancing
    ; Assets and Liabilities at the opening, but now does it using a 
    ; separate Fund.
    2014-01-01 ! "Set up FSA for 2014"
      FSA:Assets                                                 	2000 USD
      FSA:Liabilities                                           	-2000 USD

    2014-07-15 ! "Emp1 Paystub"
      Income:Gross:Emp1                                         	-6000 USD
      Assets:Bank:Checking                                       	3000 USD
      Assets:CreditUnion:Saving                                  	1000 USD
      Assets:FedIncTaxDeposits                                    	750 USD
      Expenses:OASI                                               	375 USD
      Expenses:Medicare                                           	100 USD
      Expenses:MedicalAid                                          	10 USD
      Expenses:SalReduction:R-403b                                	600 USD
      Retirement403b:Income:EmployeeContrib                       	-600 USD
      Retirement403b:Assets:CREF                                  	600 USD
      Expenses:SalReduction:FSA                                    	75 USD
      FSA:Income:Contributions                                    	-75 USD
      FSA:Liabilities                                            	 
      Expenses:SalReduction:HealthInsurance                      	 
      Retirement403b:Income:EmployerContrib                       	-600 USD
      Retirement403b:Assets:CREF

    2014-01-01 open Expenses:Medical
    2014-07-20 ! "Direct expense from FSA"
      FSA:Expenses:Medical                                          25 USD
      FSA:Assets

    2014-07-20 ! "Medical expense from checking"
      Expenses:Medical                                             	25 USD
      Assets:Bank:Checking

    2014-07-20 ! "Medical expense reimbursed from FSA"
      Assets:Bank:Checking                                         	25 USD
      Income:ReimburseMedical
      FSA:Assets                                                   -25 USD
      FSA:Expenses:ReimburseMedical

Transfer Accounts Proposal<a id="transfer-accounts-proposal"></a>
-----------------------------------------------------------------

*By Carl Hauser*

One problem that I’ve experienced using the Fund approach is that it’s a bit too easy to make mistakes when transferring money between funds, such as in the very last transaction above. Formalizing the idea of Transfer accounts can help with this. The most common mistake is to end up with something that moves assets in both accounts in the same direction -- both up or both down as in this mistaken version of the transaction in question:

    2014-07-20 ! "Medical expense reimbursed from FSA - with mistake"
     Assets:Bank:Checking                            25 USD
     Income:ReimburseMedical
     FSA:Assets                                      25 USD
     FSA:Expenses:ReimburseMedical

This balances but isn’t what we intended. Suppose we add the idea of Transfer accounts. They live at the same place in the hierarchy as Income and Expenses and like those are non-balance-sheet accounts. But they really come into play only for transactions that involve multiple funds. There is an additional rule for transactions containing Transfer accounts: the sum of the transfers must also be zero (additional in the sense that the rule about transactions balancing within each fund is still there). So to use this we set things up a little differently:

    2014-07-15 open FSA:Transfer:Incoming:Contribution
    2014-07-15 open FSA:Transfer:Outgoing:ReimburseMedical
    2014-07-15 open Transfer:Outgoing:FSAContribution
    2014-07-15 open Transfer:Incoming:ReimburseMedical

The incorrect transaction is now flagged because sum of the transfers is `-50 USD`, not zero.

    2014-07-20 ! "Medical expense reimbursed from FSA - with mistake"
      Assets:Bank:Checking                                    25 USD
      Transfer:Incoming:ReimburseMedical
      FSA:Assets                                              25 USD
      FSA:Transfer:Outgoing:ReimburseMedical

The paycheck transaction using transfer accounts for the FSA and the retirement account amounts might look like this (after appropriate `open`s of course):

    2014-07-15 ! "Emp1 Paystub - using transfer accounts"
      Income:Gross:Emp1                                      -6000 USD
      Assets:Bank:Checking                                    3000 USD
      Assets:CreditUnion:Saving                               1000 USD
      Assets:FedIncTaxDeposits                                 750 USD
      Expenses:OASI                                            375 USD
      Expenses:Medicare                                        100 USD
      Expenses:MedicalAid                                       10 USD
      Transfer:Outgoing:Retirement403b:SalReduction          600 USD
      Retirement403b:Transfer:Incoming:EmployeeContrib
      Retirement403b:Assets:CREF                               600 USD
      Transfer:Outgoing:FSA:SalReduction                        75 USD
      FSA:Transfer:Incoming:Contributions
      FSA:Liabilities                                                   
      Expenses:SalReduction:HealthInsurance                              
      Retirement403b:Income:EmployerContrib                   -600 USD
      Retirement403b:Assets:CREF

Some might think that this is too complicated. Without changing the Transfer accounts idea or rule, you can simplify booking to just a single account per fund, `Fund:Transfer`, losing some ability for precision in reporting but without losing the ability to check correctness of transfer transactions.

Account Aliases<a id="account-aliases"></a>
-------------------------------------------

Simon Michael mentions that this is related to HLedger [<span class="underline">account aliases</span>](http://hledger.org/how-to-use-account-aliases):

> “I think this is related to the situation where you want to view entities' finances both separately and merged. Account aliases can be another way to approximate this, as in[<span class="underline">http://hledger.org/how-to-use-account-aliases</span>](http://hledger.org/how-to-use-account-aliases).”

[^1]: If you find yourself culturally challenged by our modern lifestyle, perhaps you can imagine the case of roommates, although I don’t like the reductionist view this association brings to my mind.
