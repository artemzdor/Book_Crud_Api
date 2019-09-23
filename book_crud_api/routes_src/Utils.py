#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Tuple, List

from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response

from book_crud_api.models.Book import Book
from book_crud_api.adapter_sql import create_book, find_book


async def load_book(request: Request, book: Book, id_book: int = None) -> List[Book]:
    book_find: List[Book] = await find_book(request.app["pool"], request.app["logger"], book, id_book)
    return book_find


def verify_json_post_create(data: dict, keys_verify: List[str]):
    for k, v in data.items():
        if k in keys_verify:
            if isinstance(v, (str, int)):
                pass
            else:
                return False
        else:
            return False
    return True




