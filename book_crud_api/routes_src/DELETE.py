#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from aiohttp import web
from typing import Tuple, List
from aiohttp.abc import Request
from aiohttp.web_response import Response

from book_crud_api.models.Book import Book
from book_crud_api.adapter_sql import delete_book
from book_crud_api.routes_src.Utils import load_book
from book_crud_api.routes_src.Utils import verify_json_post_create


async def delete_api(request: Request) -> Response:
    text: str = await request.text()
    data: dict = dict()
    try:
        data = json.loads(text)
    except Exception as e:
        return web.json_response({"massage": "Error decode json", "error": f"{e}", "successful": False}, status=415)

    if not verify_json_post_create(data, ["id"]):
        return web.json_response({"massage": "Error keys json", "error": 'id', "successful": False}, status=422)

    book: Book = Book(**data)
    book_find: List[Book] = await load_book(request, book, id_book=book.get_id())

    if book_find:
        # в случае повторного удаления
        if book_find[0].get_removed():
            return web.json_response({"id": f"{book.get_id()}", "successful": True}, status=200)
        else:
            await delete_book(request.app["pool"], request.app["logger"], book)
            return web.json_response({"id": f"{book.get_id()}", "successful": True}, status=200)
    else:
        return web.json_response({"id": f"{book.get_id()}", "error": f"Not found Book", "successful": False},
                                 status=460)
