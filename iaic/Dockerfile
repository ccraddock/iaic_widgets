FROM ubuntu:17.10
MAINTAINER sr

ADD . /

RUN apt-get update
RUN apt-get install -y python3-pip   
RUN apt-get install -y dcmtk && \
    pip3 install pydicom && \
    pip3 install numpy && \
    pip3 install glob3 && \
    apt-get install -y python3-tk
    


EXPOSE 4444

ENTRYPOINT storescp -v -fe ".dcm" -xcr "echo #r> ./ip.txt && python3 ./scan.py" 4444





