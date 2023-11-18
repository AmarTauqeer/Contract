FROM python:3.9.5
WORKDIR /Contract/backend

COPY . /Contract/backend
RUN pip install -r requirements.txt
COPY . /Contract/backend
CMD ["python3", "app.py" ]



#FROM python:3.10.6
#WORKDIR /Contract/backend

#COPY . /Contract/backend

#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt

#COPY . /Contract/backend

#CMD ["python", "app.py"]

