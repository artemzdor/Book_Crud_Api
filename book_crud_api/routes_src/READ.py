#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web
from typing import List
from aiohttp.abc import Request
from aiohttp.web_response import Response

from book_crud_api.models.Book import Book
from book_crud_api.adapter_sql import read_book


async def read_api(request: Request) -> Response:
    books: List[Book] = await read_book(request.app["pool"], request.app["logger"])
    json_books: List[dict] = [i.get_dict_read() for i in books]
    if json_books:
        return web.json_response(json_books)
    else:
        return web.json_response([])
