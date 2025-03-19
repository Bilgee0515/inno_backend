
FROM ubuntu:20.04


RUN apt update && apt upgrade -y && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y python3.9 python3-pip

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python3 --version
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app/dahua_integration
RUN pip install ./NetSDK-2.0.0.1-py3-none-linux_x86_64.whl



EXPOSE 8000

RUN python3 manage.py migrate
RUN python3


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


