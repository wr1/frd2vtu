
fold:
	cfold fold 

unfold:
	cfold unfold v1.txt
	pip install -e . 



.PHONY: test test-verbose test-coverage clean

# Default Python interpreter
PYTHON = python

# Test directories and files
TEST_DIR = test
TEST_FILES = $(TEST_DIR)/test_frd2vtu.py

# Default target
all: test

# Run tests
test:
	$(PYTHON) -m pytest $(TEST_FILES)

# Run tests with verbose output
test-verbose:
	$(PYTHON) -m pytest $(TEST_FILES) -v

# Run tests with coverage report
test-coverage:
	$(PYTHON) -m pytest $(TEST_FILES) --cov=frd2vtu --cov-report=term --cov-report=html

# Run tests for a specific file category
test-small:
	$(PYTHON) -m pytest $(TEST_FILES)::test_frd_conversion[small] -v

test-medium:
	$(PYTHON) -m pytest $(TEST_FILES)::test_frd_conversion[medium] -v

test-large:
	$(PYTHON) -m pytest $(TEST_FILES)::test_frd_conversion[large] -v

test-special:
	$(PYTHON) -m pytest $(TEST_FILES)::test_frd_conversion[special] -v

# Clean up generated files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Help target
help:
	@echo "Available targets:"
	@echo "  make test            - Run all tests"
	@echo "  make test-verbose    - Run all tests with verbose output"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo "  make test-small      - Run tests for small files only"
	@echo "  make test-medium     - Run tests for medium files only"
	@echo "  make test-large      - Run tests for large files only"
	@echo "  make test-special    - Run tests for special files only"
	@echo "  make clean           - Clean up generated files"
	@echo "  make help            - Show this help message" 