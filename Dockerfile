FROM ubuntu:16.04
MAINTAINER Dell Medical School Image Analysis and Informatics Core

# TODO:
# open ports (UDP and TCP 5104) for storescp
# map container ports to system ports (using the docker command upon execution)
# investigate running container in detached mode

RUN mkdir /widget /widget_logs

RUN apt-get update && \
    apt-get install -y dcmtk && \
    apt-get install -y wget && \
    apt-get install bzip2

# install miniconda
RUN wget -q http://repo.continuum.io/miniconda/Miniconda-3.8.3-Linux-x86_64.sh && \
    bash Miniconda-3.8.3-Linux-x86_64.sh -b -p /usr/local/miniconda && \
    rm Miniconda-3.8.3-Linux-x86_64.sh

# install conda dependencies
#RUN conda install -y \
      #ipython \
      #numpy==1.11 \
      #pandas \
      #pip \
      #pyyaml \
      #scipy 

# install python dependencies
#RUN pip install \
      #patsy \
      #nibabel \
      #pydicom

copy widget/* /widget/
RUN chmod -R +x /widget/*

ENTRYPOINT ["/widget/start-dcm-server"]
