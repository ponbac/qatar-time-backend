# docker build -t qatar-backend:0.1 .
# docker run --rm -p 443:443 qatar-backend:0.1
FROM python:3.9.7

WORKDIR /code
ENV PYTHONPATH=/code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python3", "realtime_server.py"]