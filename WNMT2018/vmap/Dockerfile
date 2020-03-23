FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y \
            build-essential \
            cmake \
            git-core \
            pkg-config \
            automake \
            libtool \
            wget \
			zlib1g-dev \
            python-dev \
            libbz2-dev

WORKDIR /root

RUN git clone --branch RELEASE-4.0 https://github.com/moses-smt/mosesdecoder.git
WORKDIR /root/mosesdecoder

RUN make -f contrib/Makefiles/install-dependencies.gmake

RUN ./compile.sh

WORKDIR /root

RUN git clone https://github.com/clab/fast_align.git
WORKDIR /root/fast_align
RUN mkdir build ; cd build ; cmake .. ; make

COPY buildPT.sh /root
COPY paste.py /root
COPY filter.py /root

ENTRYPOINT ["/root/buildPT.sh"]
