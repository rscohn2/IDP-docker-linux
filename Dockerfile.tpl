{% if os_name == "centos" %}
FROM centos:latest
RUN yum install -y \
    bzip2 \
    wget
{% elif os_name == "ubuntu" %}
FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    bzip2 \
    wget
{% endif %}

MAINTAINER Robert Cohn <Robert.S.Cohn@intel.com>

# do not use latest because of 4.2.11 issue: https://github.com/conda/conda/issues/3775
ARG MINICONDA_PACKAGE=Miniconda3-4.1.11-Linux-x86_64.sh
ARG MINICONDA=/usr/local/miniconda3
ARG CHANNEL=intel
ARG COMMON_CORE_PKGS="icc_rt tcl mkl openssl sqlite tk xz zlib"
ARG COMMON_FULL_PKGS="impi_rt libsodium pixman yaml hdf5 libpng libxml2 zeromq freetype fontconfig cairo"
ARG INSTALL_LOCATION=/opt/conda

# Add Tini
ENV TINI_VERSION v0.10.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# The docker layers are structured to share as much as possible between
# images so downloads are smaller if you are using multiple images. For a given
# OS, there is a shared layer that contains MKL, miniconda, and other common
# components. Python2 or 3 core packages are installed in a layer on top. Full
# packages are installed in a layer on top of core.

ENV PATH $INSTALL_LOCATION/bin:$PATH

# Use miniconda to install intel python
RUN cd /tmp \
    && wget -q https://repo.continuum.io/miniconda/$MINICONDA_PACKAGE \
    && chmod +x /tmp/$MINICONDA_PACKAGE \
    && /tmp/$MINICONDA_PACKAGE -b -p $MINICONDA \
    && rm /tmp/$MINICONDA_PACKAGE \
    && $MINICONDA/bin/conda update -y -q conda

# Download packages that are common to python2 &3 so they will be in a separate layer and shared
RUN $MINICONDA/bin/conda config --add channels $CHANNEL \
    && ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp_common ${COMMON_CORE_PKGS} \
    && $MINICONDA/bin/conda env remove -n idp_common

# Create IDP environment
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp intelpython{{pyver}}_core={{rev}} python={{pyver}}
LABEL org.label-schema.intel-python-package="intelpython{{pyver}}_core={{rev}}"

{% if variant == "full" %}
# Download packages that are common to python2 &3 so they will be in a separate layer and shared
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp_common ${COMMON_FULL_PKGS} \
    && $MINICONDA/bin/conda env remove -n idp_common
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda install -q -y -n idp intelpython{{pyver}}_full={{rev}} python={{pyver}}
LABEL org.label-schema.intel-python-package="intelpython{{pyver}}_full={{rev}}"
{% endif %}

RUN ln -s $MINICONDA/envs/idp $INSTALL_LOCATION

LABEL org.label-schema.build-date="{{build_date}}" \
      org.label-schema.name="Intel Distribution for Python" \
      org.label-schema.description="Python distribution containing scipy stack and related components" \
      org.label-schema.url="https://software.intel.com/en-us/intel-distribution-for-python" \
      org.label-schema.vcs-ref="{{vcs_ref}}" \
      org.label-schema.vcs-url="https://github.com/rscohn2/IDP-docker-linux" \
      org.label-schema.vendor="Intel" \
      org.label-schema.schema-version="1.0"
