{% extends "Dockerfile.base.tpl" %}
{% block os_setup %}

FROM centos:latest
RUN yum install -y \
    bzip2 \
    wget

{% endblock %}
