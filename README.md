# IDP-docker-ubuntu

Build/test/publish docker images for intel python and latest ubuntu
LTS (16.04 when I wrote this).

It uses miniconda as the installer and creates a conda environment in
/usr/local/miniconda3/envs/idp. Start a docker container for intel python 3.5 with:

    docker run -i -t rscohn2/idp3.ubuntu /idp/bin/python

Builds:
- rscohn2/idp2.ubuntu
- rscohn2/idp2.ubuntu:latest
- rscohn2/idp2.ubuntu:2017b1
- rscohn2/idp3.ubuntu
- rscohn2/idp3.ubuntu:latest
- rscohn2/idp3.ubuntu:2017b1

[![Build Status](https://travis-ci.org/rscohn2/IDP-docker-ubuntu.svg?branch=master)](https://travis-ci.org/rscohn2/IDP-docker-ubuntu)
