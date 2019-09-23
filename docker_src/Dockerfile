FROM python:3.7.4

MAINTAINER Artem Zdor "artemzdor@gmail.com"

RUN mkdir -p /usr/src/Book_Crud_Api

COPY ./Book_Crud_Api/ /usr/src/Book_Crud_Api

EXPOSE 8080

WORKDIR /usr/src/Book_Crud_Api/book_crud_api

ENV PATH_CONFIG_JSON /usr/src/Book_Crud_Api/book_crud_api/config.json
ENV PYTHONPATH /usr/src/Book_Crud_Api

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
