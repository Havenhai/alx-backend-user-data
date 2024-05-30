#!/usr/bin/env python3
""" script of filtered_logger.py """
import re
from typing import List
import logging
import os
from mysql.connector import connection

PII_FIELDS = (
    "name",
    "email",
    "phone",
    "ssn",
    "password",
)


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str,
) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        pattern = re.compile(
            rf"{re.escape(field)}=.*?{re.escape(separator)}",
        )
        replacement = f"{field}={redaction}{separator}"
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record, redacting specified fields."""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR,
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """creates user_data logger"""
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> connection.MySQLConnection:
    """returns a connector to the database"""
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    return connection.MySQLConnection(
        host=host,
        username=username,
        password=password,
        database=db_name,
    )


def main():
    """main function"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        line = ""
        for key, value in row.items():
            line += f"{key}={value}; "
        logger.info(line)


if __name__ == "__main__":
    main()
