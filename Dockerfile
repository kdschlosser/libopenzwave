FROM ubuntu:latest
MAINTAINER Kevin G Schlosser
ENV LIB_OPENZWAVE_DOCKER 1
RUN apt-get update && apt-get dist-upgrade -y >/dev/null
RUN apt-get install -y --no-install-recommends make sudo apt-utils >/dev/null
ADD . /home/libopenzwave
WORKDIR /home/libopenzwave
RUN make docker-deps >/dev/null
RUN make libopenzwave.gzip >/dev/null
RUN make venv-dev-autobuild-tests
#RUN make venv-pypi-autobuild-tests
#RUN apt-get install --force-yes -y pkg-config >/dev/null
#RUN make venv-git_shared-autobuild-tests
#RUN apt-get remove --force-yes -y pkg-config >/dev/null
RUN make venv-pypilive-autobuild-tests
