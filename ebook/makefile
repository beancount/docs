CHAPTERS= \
  index.md \
  command_line_accounting_in_context.md \
  the_double_entry_counting_method.md \
  installing_beancount.md \
  running_beancount_and_generating_reports.md \
  getting_started_with_beancount.md \
  beancount_language_syntax.md \
  beancount_options_reference.md \
  precision_tolerances.md \
  beancount_query_language.md \
  beancount_cheat_sheet.md \
  how_inventories_work.md \
  exporting_your_portfolio.md \
  tutorial_example.md \
  beancount_history_and_credits.md \
  a_comparison_of_beancount_and_ledger_hledger.md \
  fetching_prices_in_beancount.md \
  importing_external_data.md \
  command_line_accounting_cookbook.md \
  trading_with_beancount.md \
  stock_vesting_in_beancount.md \
  sharing_expenses_with_beancount.md \
  how_we_share_expenses.md \
  health_care_expenses.md \
  calculating_portolio_returns.md \
  beancount_scripting_plugins.md \
  beancount_design_doc.md \
  ledgerhub_design_doc.md \
  external_contributions.md \
  a_proposal_for_an_improvement_on_inventory_booking.md \
  settlement_dates_in_beancount.md \
  balance_assertions_in_beancount.md \
  fund_accounting_with_beancount.md \
  rounding_precision_in_beancount.md \
  beancount_v3.md \
  installing_beancount_v3.md \
  beancount_v3_dependencies.md

# CHAPTERS= \
#   index.md \
#   command_line_accounting_in_context.md \
#   beancount_v3_dependencies.md

DOCS_DIR=../docs
PREPROCESSED_DIR=preprocessed

SOURCES=$(foreach c,$(CHAPTERS),$(DOCS_DIR)/$c)
PREPROCESSED=$(foreach c,$(CHAPTERS),preprocessed/$c)

all: clean preprocess ebook

clean:
	rm -rf "$(PREPROCESSED_DIR)" beancount.html

$(PREPROCESSED_DIR):
	mkdir -p "$@"

$(PREPROCESSED_DIR)/%.md: $(DOCS_DIR)/%.md $(PREPROCESSED_DIR)
	cp "$<" "$@"
# cp -R $(basename $<) $(PREPROCESSED_DIR)/ || true
	sed -i -e 's@<a id="\(.*\)"></a>@<a id="$(notdir $<).\1"></a>@' $@
	sed -i -e 's@](#\(.*\))@](#$(notdir $<).\1)@' $@
	sed -i -e 's@](\(.*\.md\))@](#\1\.title)@' $@

preprocess: $(PREPROCESSED)
	@echo "Preprocess done!"

ebook:	beancount.html
	@echo "Ebook done!"

beancount.html: preprocess
	pandoc \
		--from markdown \
		--to html \
		--resource-path $(DOCS_DIR) \
		--standalone \
		--self-contained \
		--metadata-file=metadata.yaml \
		--output $@ \
		$(PREPROCESSED)

.PHONY: all preprocess clean ebook
.DELETE_ON_ERROR:
