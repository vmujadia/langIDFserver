FROM python:3.8


WORKDIR langIDFserver

COPY requirements.txt .
COPY load_models_langidentify.py .
COPY run_server.py .
COPY tokenization.py .

COPY dependencies.sh .
COPY start_server.sh .

RUN pip install -r requirements.txt

RUN sh dependencies.sh 

EXPOSE 8046

CMD sh start_server.sh
