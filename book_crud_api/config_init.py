#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path


def get_version() -> str:
    return "1.0.0"


def get_app_info() -> str:
    return "Book CRUD API"


def get_environ_path_config_json() -> str:
    return "PATH_CONFIG_JSON"


def verify_config_json(data: dict) -> bool:
    if not isinstance(data, dict):
        raise TypeError("verify_config_json: Error type dict")
    if "pg_connect" not in data:
        raise RuntimeError("verify_config_json: Not found key: pg_connect")
    if not isinstance(data["pg_connect"], dict):
        raise TypeError("verify_config_json: Error type dict: pg_connect")
    if "host" not in data["pg_connect"]:
        raise RuntimeError("verify_config_json: Not found key: pg_connect.host")
    if "port" not in data["pg_connect"]:
        raise RuntimeError("verify_config_json: Not found key: pg_connect.port")
    if "user" not in data["pg_connect"]:
        raise RuntimeError("verify_config_json: Not found key: pg_connect.user")
    if "password" not in data["pg_connect"]:
        raise RuntimeError("verify_config_json: Not found key: pg_connect.password")
    if "database" not in data["pg_connect"]:
        raise RuntimeError("verify_config_json: Not found key: pg_connect.database")
    return True


def load_config() -> dict:
    path_str: str = os.environ.get(get_environ_path_config_json())

    if not path_str:
        raise RuntimeError(f"Not environ: {get_environ_path_config_json()}")

    path: Path = Path(path_str)
    del path_str
    if path.exists() and path.is_file():
        data_config: dict = json.loads(path.read_text())
        if verify_config_json(data=data_config):
            return data_config
    else:
        raise RuntimeError(f"Not Found config file: {path.absolute()}")
