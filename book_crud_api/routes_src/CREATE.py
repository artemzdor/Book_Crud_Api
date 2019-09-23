#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response

async def create_api(request: Request) -> Response:
    data_json: dict = request.json()
    web.json_response(data=data_json)
