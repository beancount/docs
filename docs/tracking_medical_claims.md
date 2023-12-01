# Tracking Out-of-Network Medical Claims in Beancount<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca) - Updated: November 2023

Let's illustrate how one might handle dealing with medical treatment with insurance and HSA claims. Let's use an example of psychotherapy sessions, received out-of-network and paid upfront out of pocket and reimbursed later.

When a session is received, it is booked to receivables and payables:


       2023-09-06 * "Dr. Freud" "Session" #freud-2023-09
         Assets:AccountsReceivable:Psychotherapy     260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  -260.00 USD

       2023-09-11 * "Dr. Freud" "Session" #freud-2023-09
         Assets:AccountsReceivable:Psychotherapy     260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  -260.00 USD

Later on, some payments are made for it, clearing the payables:


       2023-09-12 * "ZELLE SENT" #freud-2023-09
         Assets:US:BofA:Checking                     -520.00 USD
         Liabilities:AccountsPayable:Psychotherapy    520.00 USD

And so on, for the entire month:


       2023-09-20 * "Dr. Freud" "Session" #freud-2023-09
         Assets:AccountsReceivable:Psychotherapy     260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  -260.00 USD

       2023-09-23 * "ZELLE SENT" #freud-2023-09
         Assets:US:BofA:Checking                     -260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  260.00 USD


       2023-09-27 * "Dr. Freud" "Session" #freud-2023-09
         Assets:AccountsReceivable:Psychotherapy     260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  -260.00 USD

       2023-09-28 * "ZELLE SENT" #freud-2023-09
         Assets:US:BofA:Checking                     -260.00 USD
         Liabilities:AccountsPayable:Psychotherapy  260.00 USD

At the end of the month, a claim form is produced by the therapist. We file the claim with the insurance company, clearing the receivable and shifting the remaining portion to a insurance company check to be issued:


       2023-09-28 * "Claim for September filed with insurance" #freud-2023-09
         Assets:AccountsReceivable:Psychotherapy  -1040.00 USD
         Expenses:Mental:Psychotherapy              312.00 USD
         Assets:AccountsReceivable:Anthem           728.00 USD

Eventually, an EOB is produced to confirm how much is covered (in this example, 70%, which was known from the terms) and a check is received and deposited at the bank:


       2023-10-24 * "ATM CHECK DEPOSIT" #freud-2023-09
         Assets:US:BofA:Checking             728.00 USD
         Assets:AccountsReceivable:Anthem   -728.00 USD

At this stage we know the amount of the remaining portion eligible to be paid from the HSA, so we file a claim to the HSA company, once again booking them to a receivable and a payable:


       2023-10-25 * "HealthEquity" "Filed for reimbursement" #freud-2023-09
         Liabilities:AccountsPayable:HealthEquity  -312.00 USD
         Assets:AccountsReceivable:HealthEquity     312.00 USD

The HSA company makes a direct deposit to our checking account:


       2023-11-01 * "BofA bank (Claim ID:1234567-890); EFT to bank" #freud-2023-09
         Assets:US:HealthEquity:Cash               -312.00 USD
         Liabilities:AccountsPayable:HealthEquity   312.00 USD

And on the bank side when we import this transaction we book it against the receivable:


       2023-11-01 * "HEALTHEQUITY INC" #freud-2023-09
         Assets:US:BofA:Checking                    312.00 USD
         Assets:AccountsReceivable:HealthEquity    -312.00 USD

The final result is that the HSA was used to cover the uninsured portion of the cost.

    |-- Assets                       
    |   |-- AccountsReceivable       
    |   |   |-- Anthem                
    |   |   |-- HealthEquity         
    |   |   `-- Psychotherapy        
    |   `-- US                       
    |       |-- HealthEquity         
    |       |   `-- Cash                  -312.00               USD
    |       `-- BofA                   
    |           `-- Checking         
    |-- Expenses                     
    |   `-- Mental                   
    |       `-- Psychotherapy              312.00               USD
    `-- Liabilities                  
        `-- AccountsPayable          
            |-- HealthEquity         
            `-- Psychotherapy        

    Net Income: (-312.00 USD)

There are some flaws with the approach above:

-   The amount covered by insurance is known ahead of time; in many cases the amount is not known before the EOB is issued by the insurance (after all that's what it's for, it's the "Explanation of Benefits"). This would require modifying the above.
