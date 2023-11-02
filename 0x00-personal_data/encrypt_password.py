#!/usr/bin/env python3
"""
This is a simple module and it only has
one function called hash_password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Creates a password hash

    Args:
        password (str): plain password

    Returns:
        bytes: salted, hashed password
    """
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid

    Args:
        hashed_password (bytes): hashed password
        password (str): plain text password

    Returns:
        bool: _description_
    """
    return bcrypt.checkpw(password, hashed_password)
