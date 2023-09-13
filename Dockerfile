FROM python:3.9

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod -R 777 ./