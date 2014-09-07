all: bin/mio

bin/mio:
	@rpython mio/main.py
