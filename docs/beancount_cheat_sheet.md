Beancount Syntax Cheat Sheet<a id="title"></a>
==============================================

<table><tbody><tr class="odd"><td><p><em>Example Account Name:</em> Assets:US:BofA:Checking</p><table><tbody><tr class="odd"><td><h2 id="account-types">Account Types<a id="account-types"></a></h2><table><tbody><tr class="odd"><td><p>Assets</p><p>Liabilities</p><p>Income</p><p>Expenses</p><p>Equity</p></td><td><p><strong>+</strong></p><p><strong>-</strong></p><p><strong>-</strong></p><p><strong>+</strong></p><p><strong>-</strong></p></td></tr></tbody></table></td><td><h2 id="commodities">Commodities<a id="commodities"></a></h2><p><em>All in CAPS:</em></p><p>USD, EUR, CAD, AUD</p><p>GOOG, AAPL, RBF1005</p><p>HOME_MAYST, AIRMILES<br />
HOURS</p></td></tr></tbody></table><h2 id="directives">Directives<a id="directives"></a></h2><blockquote><p><em>General syntax:</em></p><p><strong>YYYY-MM-DD <em>&lt;directive&gt; &lt;arguments...&gt;</em></strong></p></blockquote><h2 id="opening-closing-accounts">Opening &amp; Closing Accounts<a id="opening-closing-accounts"></a></h2><p>2001-05-29 open Expenses:Restaurant</p><p>2001-05-29 open Assets:Checking USD,EUR <em>; Currency constraints</em></p><p>2015-04-23 close Assets:Checking</p><h2 id="declaring-commodities">Declaring Commodities<a id="declaring-commodities"></a></h2><p><em>This is optional; use this only if you want to attach metadata by currency.</em></p><p>1998-07-22 commodity AAPL<br />
name: "Apple Computer Inc."</p><h2 id="prices">Prices<a id="prices"></a></h2><p><em>Use many times to fill historical price database:</em></p><p>2015-04-30 price AAPL 125.15 USD</p><p>2015-05-30 price AAPL 130.28 USD</p><h2 id="notes">Notes<a id="notes"></a></h2><p>2013-03-20 note Assets:Checking "Called to ask about rebate"</p><h2 id="documents">Documents<a id="documents"></a></h2><p>2013-03-20 document Assets:Checking "path/to/statement.pdf"</p></td><td>

  <h2 id="transactions">Transactions<a id="transactions"></a></h2><p>2015-05-30 * "Some narration about this transaction"<br />
Liabilities:CreditCard -101.23 USD<br />
Expenses:Restaurant 101.23 USD</p><p>2015-05-30 ! "Cable Co" "Phone Bill" #tag ˆlink</p><p>id: "TW378743437" <em>; Meta-data</em><br />
Expenses:Home:Phone 87.45 USD<br />
Assets:Checking <em>; You may leave one amount out</em></p>

  <h3 id="postings">Postings<a id="postings"></a></h3><p>... 123.45 USD <em>Simple</em><br />
... 10 GOOG <strong>{502.12 USD}</strong> <em>With per-unit cost<br />
</em> ... 10 GOOG <strong>{{5021.20 USD}}</strong> <em>With total cost</em></p><p>... 10 GOOG <strong>{502.12 # 9.95 USD}</strong> <em>With both costs</em><br />
... 1000.00 USD <strong>@ 1.10 CAD</strong> <em>With per-unit price</em><br />
... 1000.00 USD <strong>@ 1100.00 CAD</strong> <em>With total price</em><br />
... 10 GOOG {502.12 USD} @ 1.10 CAD <em>With cost &amp; price</em><br />
... 10 GOOG {502.12 USD, <strong>2014-05-12</strong>} <em>With date</em><br />
<strong>!</strong> ... 123.45 USD ... <em>With flag</em></p>

  <h2 id="balance-assertions-and-padding">Balance Assertions and Padding<a id="balance-assertions-and-padding"></a></h2><p><em>Asserts the amount for only the given currency:</em></p><p>2015-06-01 balance Liabilities:CreditCard -634.30 USD</p><p><em>Automatic insertion of transaction to fulfill the following assertion:</em></p><p>YYYY-MM-DD pad Assets:Checking Equity:Opening-Balances</p><h2 id="events">Events<a id="events"></a></h2><p>YYYY-MM-DD event "location" "New York, USA"<br />
YYYY-MM-DD event "address" "123 May Street"</p><h2 id="options">Options <a id="options"></a></h2><p>option "title" "My Personal Ledger"</p><p><em>See <a href="beancount_options_reference.md"><span class="underline">this doc</span></a> for the full list of supported options.</em></p><h2 id="other">Other<a id="other"></a></h2><p>pushtag #trip-to-peru</p><p>...</p><p>poptag #trip-to-peru</p><p>; Comments begin with a semi-colon</p></td></tr></tbody></table>
