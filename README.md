# IDP-docker-ubuntu

Build/test/publish docker images for intel python with various linux distro's (centos,ubuntu)

Start a docker container for intel python 3.5 on ubuntu with:

    docker run -i -t rscohn2/idp3_core.ubuntu python

## Images

Image names follow this convention:

rscohn2/idp{2,3}_{core,full}.{centos,ubuntu}

There is python 2 & 3, core is python + scipy and dependences, full is the
full intel distribution, using the latest centos or ubuntu.

### Current published images

rscohn2/idp2_full.centos: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp2_full.centos.svg)](https://microbadger.com/images/rscohn2/idp2_full.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp2_full.centos.svg)](https://microbadger.com/images/rscohn2/idp2_full.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp2_full.centos.svg)](https://microbadger.com/images/rscohn2/idp2_full.centos "Get your own image badge on microbadger.com")

rscohn2/idp2_core.centos: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp2_core.centos.svg)](https://microbadger.com/images/rscohn2/idp2_core.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp2_core.centos.svg)](https://microbadger.com/images/rscohn2/idp2_core.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp2_core.centos.svg)](https://microbadger.com/images/rscohn2/idp2_core.centos "Get your own image badge on microbadger.com")

rscohn2/idp3_full.centos: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp3_full.centos.svg)](https://microbadger.com/images/rscohn2/idp3_full.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp3_full.centos.svg)](https://microbadger.com/images/rscohn2/idp3_full.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp3_full.centos.svg)](https://microbadger.com/images/rscohn2/idp3_full.centos "Get your own image badge on microbadger.com")

rscohn2/idp3_core.centos: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp3_core.centos.svg)](https://microbadger.com/images/rscohn2/idp3_core.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp3_core.centos.svg)](https://microbadger.com/images/rscohn2/idp3_core.centos "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp3_core.centos.svg)](https://microbadger.com/images/rscohn2/idp3_core.centos "Get your own image badge on microbadger.com")

rscohn2/idp2_full.ubuntu: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp2_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_full.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp2_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_full.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp2_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_full.ubuntu "Get your own image badge on microbadger.com")

rscohn2/idp2_core.ubuntu: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp2_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_core.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp2_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_core.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp2_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp2_core.ubuntu "Get your own image badge on microbadger.com")

rscohn2/idp3_full.ubuntu: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp3_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_full.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp3_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_full.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp3_full.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_full.ubuntu "Get your own image badge on microbadger.com")

rscohn2/idp3_core.ubuntu: 
[![](https://images.microbadger.com/badges/version/rscohn2/idp3_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_core.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/commit/rscohn2/idp3_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_core.ubuntu "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/rscohn2/idp3_core.ubuntu.svg)](https://microbadger.com/images/rscohn2/idp3_core.ubuntu "Get your own image badge on microbadger.com")


## How to build the images

To build all images do:

    python build.py 

You can use command line arguments to build a subset. To see the help:

    python build.py --help

## How python is installed into the image

It uses miniconda as the installer and creates a conda environment in
/usr/local/miniconda3/envs/idp. A symbolic link is created from
/opt/conda and /opt/conda is added to the path.

## How the docker images are built

build.py generates Dockerfiles for each of the variants, using jinja2 to
subtitute the info specific to the image. Dockerfile.tpl is the jinja2
template. The docker layers are structured to share as much as possible between
images so downloads are smaller.

## Publishing images

Images are built on https://travis-ci.org/rscohn2/IDP-docker-linux and
published to https://hub.docker.com/r/rscohn2/

[![Build Status](https://travis-ci.org/rscohn2/IDP-docker-linux.svg?branch=master)](https://travis-ci.org/rscohn2/IDP-docker-linux)
