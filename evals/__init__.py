"""Runnable evals for DeployerX playbooks.

Every playbook ships a machine-checkable eval suite (`evals/cases.json`).
Scoring is deterministic — no model or network needed — so the same rules
grade a Path A (browser, zero-cost) run and an API run identically.

    python3 -m evals.run list
    python3 -m evals.run prepare <playbook>   # zero-cost: paste bundle + responses skeleton
    python3 -m evals.run score <playbook> --responses <file>
    python3 -m evals.run api <playbook>       # generate replies via the Anthropic API, then score
    python3 -m evals.run selftest             # score bundled fixtures (runs in CI via `make check`)
"""
