FROM python:3.9.2-alpine
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY fetch-sungrow-inverter.py .
CMD ["sh", "-c", "while true; do python3 fetch-sungrow-inverter.py; sleep 60; done"]