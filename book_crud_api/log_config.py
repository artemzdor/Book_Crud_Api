#!/usr/bin/env python3
# -*- coding: utf-8 -*-

dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 50 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "myFormatter",
            "filename": "logs.log"
        }
    },
    "loggers": {
        "deviceApp": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}