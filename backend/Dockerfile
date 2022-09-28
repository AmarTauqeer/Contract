FROM python:3.10.6
WORKDIR /Contract/backend

COPY . /Contract/backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
