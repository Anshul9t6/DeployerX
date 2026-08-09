.PHONY: check site coverage resolve seed-in status help eval eval-selftest

help:
	@echo "make status         session brief + refresh STATUS.md metrics"
	@echo "make check          validate hierarchy + site data sync + eval selftest"
	@echo "make site           regenerate docs/data/progress.json"
	@echo "make coverage       print coverage report"
	@echo "make resolve        example: make resolve ARGS='in uttar-pradesh varanasi'"
	@echo "make eval           example: make eval ARGS='api whatsapp-shop-faq --locale in/rajasthan/jaipur'"
	@echo "make eval-selftest  grade bundled eval fixtures (no network)"
	@echo "make seed-in        seed missing India L2 stubs"

status:
	python3 scripts/status.py

check:
	python3 scripts/validate.py
	python3 -m evals.run selftest

eval:
	python3 -m evals.run $(ARGS)

eval-selftest:
	python3 -m evals.run selftest

site:
	python3 scripts/generate_site_data.py

coverage:
	python3 scripts/coverage.py

resolve:
	python3 -m decision.resolve $(ARGS)

seed-in:
	python3 scripts/seed_india_l2.py
