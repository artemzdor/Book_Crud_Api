#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web
from typing import Dict
from logging import Logger
from aiohttp.abc import Request
from aiohttp.web_response import Response
from book_crud_api.config_init import get_version
from book_crud_api.config_init import get_app_info


async def version_api(request: Request) -> Response:
    data: Dict[str, str] = {"version": get_version(), "app": get_app_info()}
    logger: Logger = request.app["logger"]
    logger.info("run version_json")
    return web.json_response(data)



