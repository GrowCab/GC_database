FROM python:3.8-alpine3.12

RUN apk add --no-cache build-base
RUN pip3 install cython



WORKDIR /backend
COPY . /backend

RUN pip3 install -r requirements.txt
RUN pip3 install .
CMD [ "./build_database.py" ]
CMD ["flask", "run", "--host", "0.0.0.0"]
