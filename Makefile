.PHONY: check site coverage resolve seed-in status help

help:
	@echo "make status     session brief + refresh STATUS.md metrics"
	@echo "make check      validate hierarchy + site data sync"
	@echo "make site       regenerate docs/data/progress.json"
	@echo "make coverage   print coverage report"
	@echo "make resolve    example: make resolve ARGS='in uttar-pradesh varanasi'"
	@echo "make seed-in    seed missing India L2 stubs"

status:
	python3 scripts/status.py

check:
	python3 scripts/validate.py

site:
	python3 scripts/generate_site_data.py

coverage:
	python3 scripts/coverage.py

resolve:
	python3 -m decision.resolve $(ARGS)

seed-in:
	python3 scripts/seed_india_l2.py
