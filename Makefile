# Build, package, test, and clean
PROJECT=sphinx_gmt
FORMAT_FILES=$(PROJECT) setup.py doc/conf.py
LINT_FILES=$(PROJECT) setup.py

help:
	@echo "Commands:"
	@echo ""
	@echo "    install       install in editable mode"
	@echo "    package       build source and wheel distributions"
	@echo "    check         run code quality checks (black and pylint)"
	@echo "    format        run black to automatically format the code"
	@echo "    clean         clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

package:
	python -m build --sdist --wheel

format:
	black $(FORMAT_FILES)

check:
	black --check $(FORMAT_FILES)
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -type d -name  "__pycache__" -exec rm -rv {} +
	rm -rvf build dist MANIFEST *.egg-info .coverage .cache
	rm -rvf $(TESTDIR)
	rm -rvf baseline
