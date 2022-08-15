FROM python:3.7
MAINTAINER vickychen@gillygaming888.com
LABEL version = '1.0'


ARG PRODUCT_NAME='app'
RUN mkdir -p /${PRODUCT_NAME}
WORKDIR /${PRODUCT_NAME}

COPY requirements.txt .
COPY src .

RUN pip3 --no-cache-dir install -r requirements.txt
