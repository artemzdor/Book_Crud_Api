#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict, field
from datetime import datetime

@dataclass
class Book:
    id: int = field(default=0)
    name: str = field(default="")
    author: str = field(default="")
    assessment: int = field(default=0)
    removed: bool = field(default=False)
    tm_removed: datetime = field(default=None)
    tm_read: datetime = field(default=None)

    def get_dict(self) -> dict:
        return asdict(self)

    def get_dict_create_sql(self) -> dict:
        data: dict = self.get_dict()
        data.pop("id")
        data.pop("tm_read")
        return data

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_author(self) -> str:
        return self.author

    def get_removed(self) -> bool:
        return self.removed

    def get_assessment(self) -> int:
        return self.assessment

    def get_tm_read(self) -> float:
        return self.tm_read

    def get_tm_removed(self) -> float:
        return self.tm_removed

