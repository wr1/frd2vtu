.PHONY: all test test-verbose test-coverage readme-coverage clean help

PYTHON = python
TEST_FILES = test/test_frd2vtu.py

all: test

test:
	$(PYTHON) -m pytest $(TEST_FILES)

test-verbose:
	$(PYTHON) -m pytest $(TEST_FILES) -v

test-coverage:
	$(PYTHON) -m pytest $(TEST_FILES) --cov=frd2vtu --cov-report=term --cov-report=html

readme-coverage:
	$(PYTHON) scripts/regenerate_readme_coverage.py

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

help:
	@echo "Targets:"
	@echo "  make test            Run tests"
	@echo "  make test-verbose    Run tests (verbose)"
	@echo "  make test-coverage   Run tests with coverage"
	@echo "  make readme-coverage Regenerate README FRD status table"
	@echo "  make clean           Remove caches and coverage artifacts"
	@echo "  make help            Show this message"