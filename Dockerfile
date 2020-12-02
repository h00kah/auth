FROM python:3.8-alpine

ADD requirements.txt ./

RUN apk add --no-cache --virtual .build-deps gcc make musl-dev python3-dev libffi-dev libressl-dev py3-pynacl \
 && python -m pip install -r requirements.txt \
 && apk del .build-deps gcc musl-dev python3-dev libffi-dev libressl-dev

RUN mkdir -p ~/.postgresql && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O ~/.postgresql/root.crt && \
chmod 0600 ~/.postgresql/root.crt

ADD . ./

ENTRYPOINT [ "python", "-m", "auth" ]