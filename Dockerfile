FROM python:3.8-alpine

ADD . ./

RUN apk add --no-cache --virtual .build-deps gcc make musl-dev python3-dev libffi-dev libressl-dev py3-pynacl \
 && python -m pip install -r requirements.txt \
 && apk del .build-deps gcc musl-dev python3-dev libffi-dev libressl-dev

ENTRYPOINT [ "python", "-m", "auth" ]