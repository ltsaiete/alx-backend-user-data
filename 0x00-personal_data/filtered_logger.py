#!/usr/bin/env python3
"""
This is a simple module and it only has
one function called filter_datum
"""


import logging
from typing import List
import re
from os import getenv
import mysql.connector


PERSONAL_DATA_DB_HOST = getenv('PERSONAL_DATA_DB_HOST', default='localhost')
PERSONAL_DATA_DB_USERNAME = getenv('PERSONAL_DATA_DB_USERNAME', default='root')
PERSONAL_DATA_DB_PASSWORD = getenv('PERSONAL_DATA_DB_PASSWORD', default='root')
PERSONAL_DATA_DB_NAME = getenv('PERSONAL_DATA_DB_NAME', default='holberton')
PII_FIELDS = ['name', 'email', 'phone', 'password', 'ip']


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """returns the log message obfuscated

    Args:
        fields (List[str]): all fields to obfuscate
        redaction (str):  by what the field will be obfuscated
        message (str): the log line
        separator (str): by which character is separating
            all fields in the log line (message)

    Returns:
        str: the log message obfuscated
    """
    obfuscated_message = []

    for value in message.split(separator):
        obfuscated_message.append(re.sub(
            "=.*", "=" + redaction, value) if re.match(
                f'{"|".join(fields)}', value) else value)

    return ';'.join(obfuscated_message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filtered_record = record
        filtered_record.msg = filter_datum(self.fields, self.REDACTION,
                                           record.msg, self.SEPARATOR)
        return super().format(filtered_record)

def get_logger():
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db():
    db = mysql.connector.connect(
            host=PERSONAL_DATA_DB_HOST,
            user=PERSONAL_DATA_DB_USERNAME,
            password=PERSONAL_DATA_DB_PASSWORD,
            database=PERSONAL_DATA_DB_NAME
        )
    return db


def main():
    FIELDS = ['name', 'email', 'phone', 'ssn','password', 'ip', 'last_login', 'user_agent']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()

    logger = get_logger()


    for row in result:
        user = []
        for i in range(len(FIELDS)):
            user.append(FIELDS[i] + '=' + str(row[i]))
        logger.info(';'.join(user))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
