from python:3.10

RUN apt update 
RUN apt install -y build-essential cmake

WORKDIR /opt/unpack
COPY . /opt/unpack

RUN python -m ensurepip
RUN python -m pip install lief
RUN python -m pip install kaitaistruct

WORKDIR /opt/unpack/pylegu
RUN python ./setup.py build -j4 install

WORKDIR /data

ENTRYPOINT ["/usr/local/bin/python", "/opt/unpack/unpack.py"]