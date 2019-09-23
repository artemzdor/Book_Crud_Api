#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import asyncio
import asyncpg
import logging.config
from aiohttp import web
from datetime import datetime as td
from asyncio import AbstractEventLoop
from aiohttp.web_app import Application

from book_crud_api.config_init import load_config
from book_crud_api.routes_src.READ import read_api
from book_crud_api.log_config import dictLogConfig
from book_crud_api.routes_src.CREATE import create_api
from book_crud_api.routes_src.DELETE import delete_api
from book_crud_api.routes_src.UPDATE import update_api
from book_crud_api.routes_src.version import version_api
from book_crud_api.adapter_sql import create_table_books


def get_logger() -> logging.Logger:
    logging.config.dictConfig(dictLogConfig)
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logger: logging.Logger = logging.getLogger('io_server')
    return logger


def init_routes(app: Application) -> None:
    app.add_routes([
        web.get("/", version_api),
        web.post("/", version_api),

        web.post("/create", create_api),
        web.post("/read", read_api),
        web.post("/update", update_api),
        web.post("/delete", delete_api),
    ])


async def init_app(logger: logging.Logger, config_pg: dict) -> Application:
    """Initialize the application server."""
    app: Application = web.Application()
    pool: asyncpg.pool.Pool = await asyncpg.create_pool(**config_pg["pg_connect"])
    app['pool'] = pool
    del pool
    return app


if __name__ == '__main__':
    logger: logging.Logger = get_logger()
    logger.info(f"Start {td.now()}")

    config_pg: dict = load_config()
    loop: AbstractEventLoop = asyncio.get_event_loop()
    # ждем когда подымется postgres_db
    print("Sleep 10s")
    time.sleep(10)
    print("Sleep end")
    app: Application = loop.run_until_complete(init_app(logger, config_pg=config_pg))
    app['logger'] = logger

    loop.run_until_complete(create_table_books(app['pool'], logger=logger))
    init_routes(app=app)

    print(f"Start {td.now()}")
    web.run_app(app)
    print(f"Stop {td.now()}")
    logger.info(f"Stop {td.now()}")

