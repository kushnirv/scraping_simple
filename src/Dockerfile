FROM python:3.6.2-alpine

RUN apk update && apk add -U postgresql-dev gcc python3-dev musl-dev

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./ /usr/src/app
WORKDIR /usr/src/app

CMD ["python", "main.py"]
