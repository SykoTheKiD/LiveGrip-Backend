FROM ubuntu:trusty

RUN sudo apt-get update
RUN sudo apt-get install software-properties-common -y
RUN sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa -y
RUN sudo apt-get update
RUN sudo apt-get install mosquitto -y

CMD mosquitto -p 8080