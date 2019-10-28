FROM python:3.7
RUN pip install redis
WORKDIR /usr/app
COPY probe.py .
CMD ["python", "./probe.py"]