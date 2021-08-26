FROM python:3.8.1

RUN mkdir -p /usr/src/main/
WORKDIR /usr/src/main/
COPY . /usr/src/main/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]