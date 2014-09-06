.PHONY: clean

all: bin/mio

clean:
	@find . -type f -name '*.pyc' -delete
	@rm -rf build dist *egg-info bin/mio

bin/mio:
	@rpython mio/main.py
