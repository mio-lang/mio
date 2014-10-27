# Docker Image for mio

FROM prologic/crux-python:latest
MAINTAINER James Mills, prologic at shortcircuit dot net dot au

# Startup
CMD ["/app/bin/mio"]

# Build/Runtime Dependencies
WORKDIR /usr/src
RUN pip install mercurial
RUN curl -# -q -O https://bitbucket.org/prologic/pypy/get/tip.tar.bz2 && \
    tar jxf tip.tar.bz2 && \
    cd prologic-pypy-* && \
    python setup-pypy.py develop && \
    python setup-rpython.py develop
RUN rm tip.tar.bz2

# Build
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt && \
    make
