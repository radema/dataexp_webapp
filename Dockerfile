# base image
# a little overkill but need it to install dot cli for dtreeviz
FROM ubuntu:18.04

# ubuntu installing - python, pip, graphviz
RUN apt-get update &&\
    apt-get install python3.7 -y &&\
    apt-get install python3-pip -y &&\
    apt-get install graphviz -y

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /streamlit-docker

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip3 install -r requirements.txt

# copying all files over
COPY . .

# cmd to launch app when container is run
CMD streamlit run webapp.py