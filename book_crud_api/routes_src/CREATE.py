#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from aiohttp import web
from typing import Tuple, List
from aiohttp.abc import Request
from aiohttp.web_response import Response

from book_crud_api.models.Book import Book
from book_crud_api.adapter_sql import create_book
from book_crud_api.routes_src.Utils import load_book
from book_crud_api.routes_src.Utils import verify_json_post_create


async def create_api(request: Request) -> Response:
    text: str = await request.text()
    data: dict = dict()
    try:
        data = json.loads(text)
    except Exception as e:
        return web.json_response({
            "massage": "Error decode json",
            "error": f"{e}",
            "successful": False
        }, status=415)

    if not verify_json_post_create(data, ["name", "author", "assessment"]):
        return web.json_response({
            "massage": "Error keys json",
            "error": 'name, author',
            "successful": False
        }, status=452)

    book: Book = Book(**data)
    book_find: Tuple[bool, List[Book]] = await load_book(request, book)

    if book_find[0]:
        book = await create_book(request.app["pool"], request.app["logger"], book)
        return web.json_response({
            "id": f"{book.get_id()}",
            "successful": True
        }, status=200)
    else:
        return web.json_response({
            "massage": "Duplicate",
            "error": ", ".join([str(i.get_id()) for i in book_find[1]]),
            "successful": False
        }, status=409)


