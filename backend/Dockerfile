FROM python:3.9.5
WORKDIR /contract/backend

COPY . /contract/backend
RUN pip install -r requirements.txt
COPY . /contract/backend
CMD ["python", "app.py" ]

