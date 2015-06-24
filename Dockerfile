FROM crux/python:onbuild

RUN rpython mio/main.py

ENTRYPOINT ["./bin/mio"]
