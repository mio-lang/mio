.PHONY: clean

all: bin/mio

clean:
	@rm -f bin/mio

bin/mio:
	@rpython mio/main.py
