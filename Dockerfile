FROM python:3.8-alpine

ADD . ./
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "app" ]