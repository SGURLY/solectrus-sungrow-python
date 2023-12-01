FROM python:3.9.2-alpine
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY main.py .
CMD ["sh", "-c", "while true; do python3 main.py; sleep 60; done"]