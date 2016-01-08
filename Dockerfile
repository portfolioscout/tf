FROM ubuntu
MAINTAINER portfolioscout

RUN echo "0.1" > /version

VOLUME /home/ruslan/tf

#ADD anaconda-tf-install.sh /
#RUN ./anaconda-tf-install.sh
RUN apt-get update
RUN apt-get -y install wget
RUN apt-get -y install bzip2
RUN apt-get -y intstall libsm6

RUN wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh
RUN bash Anaconda2-2.4.1-Linux-x86_64.sh -b
ENV PATH /root/anaconda2/bin:$PATH 
RUN conda install -y -c https://conda.anaconda.org/jjhelmus tensorflow


EXPOSE 8888

