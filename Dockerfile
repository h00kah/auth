FROM ubuntu

ADD requirements.txt ./

RUN export DEBIAN_FRONTEND="noninteractive" \
 && apt update \
 && apt install -y \
		wget \
		build-essential \
		postgresql-client \
		musl-dev \
		python3-dev \
		libffi-dev \
		openssl \
		libssl-dev \
		python3-pip \
		postgresql-common \
		libpqxx-dev \
		libpq-dev \
 && python3 -m pip install -r requirements.txt
# && apt del .build-deps gcc musl-dev python3-dev libffi-dev libressl-dev

RUN mkdir -p ~/.postgresql && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O ~/.postgresql/root.crt && \
chmod 0600 ~/.postgresql/root.crt

RUN touch production

ADD . ./
ENTRYPOINT [ "python3", "-m", "auth" ]
