FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
COPY entry_point.sh /code/entry_point.sh
COPY wait-for-it.sh /code/wait-for-it.sh
RUN pip install -r requirements.txt
ENV PYTHONPATH "/code/"
ENV DOCKER "true"