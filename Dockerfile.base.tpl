
{% block os_setup %}{% endblock %}

MAINTAINER Robert Cohn <Robert.S.Cohn@intel.com>

ARG MINICONDA=/usr/local/miniconda3
ARG CHANNEL=intel
ARG COMMON_CORE_PKGS="icc_rt tcl mkl openssl sqlite tk xz zlib"
ARG COMMON_FULL_PKGS="impi_rt libsodium pixman yaml hdf5 libpng libxml2 zeromq freetype fontconfig cairo"

# Use miniconda to install intel python
RUN cd /tmp \
    && wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && chmod +x /tmp/Miniconda3-latest-Linux-x86_64.sh \
    && /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p $MINICONDA \
    && rm /tmp/Miniconda3-latest-Linux-x86_64.sh \
    && $MINICONDA/bin/conda update -y -q conda

# Download packages that are common to python2 &3 so they will be in a separate layer and shared
RUN $MINICONDA/bin/conda config --add channels $CHANNEL \
    && ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp_common ${COMMON_CORE_PKGS} \
    && $MINICONDA/bin/conda env remove -n idp_common

# Create IDP environment
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp intelpython{{pyver}}_core python={{pyver}}

{% if variant == "full" %}
# Download packages that are common to python2 &3 so they will be in a separate layer and shared
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda create -q -y -n idp_common ${COMMON_FULL_PKGS} \
    && $MINICONDA/bin/conda env remove -n idp_common
RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda install -q -y -n idp intelpython{{pyver}}_full python={{pyver}}
{% endif %}

RUN ln -s $MINICONDA/envs/idp .
