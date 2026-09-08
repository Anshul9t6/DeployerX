.PHONY: check test site coverage resolve prompt seed-in status help eval eval-selftest mcp

help:
	@echo "make status         session brief + refresh STATUS.md metrics"
	@echo "make check          validate hierarchy + site data sync + compileall + unit tests + eval selftest"
	@echo "make test           unit tests only (tests/)"
	@echo "make site           regenerate docs/data/progress.json"
	@echo "make coverage       print coverage report"
	@echo "make resolve        example: make resolve ARGS='in rajasthan jaipur'"
	@echo "make prompt         example: make prompt ARGS='whatsapp-shop-faq --faq faq.csv --locale in/rajasthan/jaipur --out prompt.txt'"
	@echo "make eval           example: make eval ARGS='api whatsapp-shop-faq --locale in/rajasthan/jaipur'"
	@echo "make eval-selftest  grade bundled eval fixtures (no network)"
	@echo "make mcp            run the MCP server on stdio (needs: pip install mcp)"
	@echo "make seed-in        seed missing India L2 stubs"

status:
	python3 scripts/status.py

check:
	python3 scripts/validate.py
	python3 -m compileall -q decision evals deployerx_mcp scripts tests
	python3 -m unittest discover -s tests -q
	python3 -m evals.run selftest

test:
	python3 -m unittest discover -s tests -v

prompt:
	python3 -m decision.prompt $(ARGS)

eval:
	python3 -m evals.run $(ARGS)

eval-selftest:
	python3 -m evals.run selftest

mcp:
	python3 deployerx_mcp/server.py

site:
	python3 scripts/generate_site_data.py

coverage:
	python3 scripts/coverage.py

resolve:
	python3 -m decision.resolve $(ARGS)

seed-in:
	python3 scripts/seed_india_l2.py
