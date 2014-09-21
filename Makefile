.PHONY: clean docs mio

all: mio

clean:
	@rm -f bin/mio
	@make -C docs clean

docs:
	@sphinx-apidoc -f -e -T -o docs/source/api mio
	@make -C docs html

mio:
	@rpython mio/main.py
