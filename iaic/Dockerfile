FROM ubuntu:16.04
MAINTAINER sr

ADD . /
RUN apt-get update && \
    apt-get install -y dcmtk
RUN apt-get install -y python3
EXPOSE 80
EXPOSE 4444
RUN storescp -v -xcr "python3 /hello.py" 4444



