FROM python:3.8-slim-buster


WORKDIR /backend
COPY . /backend

RUN pip3 install -r requirements.txt
RUN pip3 install .
CMD [ "./build_database.py" ]
CMD ["flask", "run", "--host", "0.0.0.0"]
