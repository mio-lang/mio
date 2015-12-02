.PHONY: clean docs help mio test

PYTHON = python
RPYTHON = rpython

OPTS = "--output=bin/mio"
TARGET = "mio/main.py"

all: clean test build

help:
	@echo "clean    Remove build artifacts"
	@echo "docs     Build documentation"
	@echo "build    Build the interpreter"
	@echo "test     Run unit and integration tests"

clean:
	@rm -rf bin/mio coverage
	@make -C docs clean &> /dev/null

docs:
	@sphinx-apidoc -f -e -T -o docs/source/api mio
	@make -C docs html

build:
	$(RPYTHON) $(OPTS) $(TARGET)

test:
	$(PYTHON) setup.py test
