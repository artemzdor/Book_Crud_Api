#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import asyncpg
from datetime import datetime
from typing import List, Tuple
from book_crud_api.models.Book import Book


TABLE_NAME: str = 'books'


CREATE_TABLE: str = """
CREATE TABLE {table_name}
(
    id bigserial NOT NULL,
    name text NOT NULL,
    author text NOT NULL,
    assessment integer NOT NULL,
    removed boolean NOT NULL,
    tm_read timestamp with time zone NOT NULL DEFAULT now(),
    tm_removed timestamp with time zone,
    PRIMARY KEY (id)
)
"""


INSERT_BOOK: str = """
INSERT INTO {table_name} (name, author, assessment, removed) 
VALUES ($1::text, $2::text, $3::integer, $4::boolean)
returning id;
"""


UPDATE_BOOK: str = """
UPDATE {table_name} 
SET assessment = $1::integer 
WHERE id = $2;
"""

DELETE_BOOK: str = """
UPDATE {table_name}
SET removed = $1::boolean, tm_removed = $2::timestamp with time zone
WHERE id = $3
"""

SELECT_ALL_BOOK: str = """
SELECT *
FROM {table_name}
WHERE removed != $1
"""


def get_table_name() -> str:
    return TABLE_NAME


async def check_table(name_table: str, conn: asyncpg.connection.Connection) -> bool:
    try:
        await conn.fetchrow(f"select * from {name_table} where false;")
        return True
    except asyncpg.exceptions.UndefinedTableError as e:
        return False


async def create_table_books(pool: asyncpg.pool.Pool, logger: logging.Logger):
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        if await check_table(get_table_name(), connection):
            logger.debug(f"SUCCESS table: {get_table_name()}")
        else:
            logger.debug(f"CREATE table: {get_table_name()}")
            await connection.execute(query=CREATE_TABLE.format(table_name=get_table_name()))


async def create_book(pool: asyncpg.pool.Pool, logger: logging.Logger, book: Book) -> Book:
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        column: Tuple[str, str, int, bool] = (
            book.get_name(),
            book.get_author(),
            book.get_assessment(),
            book.get_removed(),
        )
        id_book = await connection.fetchval(INSERT_BOOK.format(table_name=get_table_name()), *column)
        book.id = id_book
        logger.info(f"CREATE book: (id: {book.get_id()}, name: {book.get_name()}, author: {book.get_author()})")
        del column, id_book
        return book


async def update_book(pool: asyncpg.pool.Pool, logger: logging.Logger, book: Book) -> Book:
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        column: Tuple[int, int] = (
            book.get_assessment(),
            book.get_id()
        )
        await connection.execute(UPDATE_BOOK.format(table_name=get_table_name()), *column)
        logger.info(f"UPDATE book: (id: {book.get_id()}, name: {book.get_name()}, "
                    f"author: {book.get_author()}), assessment: {book.get_assessment()})")
        del column
        return book


async def delete_book(pool: asyncpg.pool.Pool, logger: logging.Logger, book: Book) -> Book:
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        column: Tuple[bool, datetime, int] = (
            True,
            datetime.now(),
            book.get_id(),
        )
        await connection.execute(DELETE_BOOK.format(table_name=get_table_name()), *column)
        logger.info(f"DELETE book: (id: {book.get_id()}, name: {book.get_name()}, "
                    f"author: {book.get_author()}), assessment: {book.get_assessment()})")
        del column
        return book


async def read_book(pool: asyncpg.pool.Pool, logger: logging.Logger) -> List[Book]:
    async with pool.acquire() as connection:
        connection: asyncpg.connection.Connection
        column: Tuple[bool] = (
            True,
        )
        logger.debug("READ_BOOK")
        books = await connection.fetch(SELECT_ALL_BOOK.format(table_name=get_table_name()), *column)
        if books:
            result: List[Book] = [Book(**i) for i in books]
        else:
            result: List[Book] = list()
        del column, books
        return result

