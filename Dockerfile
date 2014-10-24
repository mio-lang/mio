# Docker Image for mio

FROM python:2
MAINTAINER James Mills, prologic at shortcircuit dot net dot au

# Startup
CMD ["/app/bin/mio"]

# Build/Runtime Dependencies
RUN pip install mercurial && \
    hg clone https://bitbucket.org/prologic/pypy /src/pypy

RUN cd /src/pypy && \
    python setup-rpython.py develop && \
    python setup-pypy.py develop

# Build
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt && \
    make clean all

# Cleanup
RUN rm -rf /src/pypy
