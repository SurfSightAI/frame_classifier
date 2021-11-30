FROM python:3.7

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE $PORT

COPY ./app .

ENTRYPOINT ["streamlit", "run", "--server.port=9090"]

CMD ["app.py"]
