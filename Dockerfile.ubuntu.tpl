{% extends "Dockerfile.base.tpl" %}
{% block os_setup %}

FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    bzip2 \
    wget
{% endblock %}
