FROM ubuntu:17.10
MAINTAINER sr

ADD . /

RUN apt-get update
RUN apt-get install -y python3-pip   
RUN apt-get install -y dcmtk && \
    pip3 install pydicom && \
    pip3 install numpy && \
    pip3 install glob3 && \
    apt-get install -y python3-tk && \
    pip3 install dash && \
    pip3 install dash-table-experiments && \
    pip3 install dash_renderer && \
    pip3 install dash_core_components & \
    pip3 install dash_html_components 
    
    


EXPOSE 4444
EXPOSE 8050

ENTRYPOINT storescp -v -fe ".dcm" -xcr "echo #r> ./ip.txt && python3 ./scan.py" 4444 





