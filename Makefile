# Build, package, test, and clean
PROJECT=sphinx_gmt
FORMAT_FILES=$(PROJECT) setup.py doc/conf.py
LINT_FILES=$(PROJECT) setup.py

help:
	@echo "Commands:"
	@echo ""
	@echo "    develop       install in editable mode"
	@echo "    check         run code quality checks (black and pylint)"
	@echo "    format        run black to automatically format the code"
	@echo "    clean         clean up build and generated files"
	@echo ""

develop:
	pip install --no-deps -e .

format:
	black $(FORMAT_FILES)

check:
	black --check $(FORMAT_FILES)
	#pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache
	rm -rvf $(TESTDIR)
	rm -rvf baseline
