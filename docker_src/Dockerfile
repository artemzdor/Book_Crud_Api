FROM python:3.7.4

MAINTAINER Artem Zdor "artemzdor@gmail.com"

RUN mkdir -p /usr/src/Book_Crud_Api

COPY ./Book_Crud_Api/ /usr/src/Book_Crud_Api

EXPOSE 8080

WORKDIR /usr/src/Book_Crud_Api/book_crud_api

CMD ["/bin/sh", "-c", "python3", "main.py"]
