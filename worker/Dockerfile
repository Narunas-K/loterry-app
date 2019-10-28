# FROM python:3.7
# RUN pip install redis
# WORKDIR /usr/app
# COPY worker-script.py .
# CMD ["python", "./worker-script.py"]
FROM python:3.7
WORKDIR /usr/app
RUN apt-get update
RUN pip install redis
RUN pip install psycopg2
RUN apt-get install -y libzmq3-dev
RUN apt-get install -y libevent-dev
RUN pip install pyzmq
RUN pip install zerorpc
COPY worker-script.py .
CMD ["python", "-u" ,"./worker-script.py"]