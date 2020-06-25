"""
Custom exceptions
"""


class CustomException(Exception):
    """
    Base custom exception
    """


class NotExist(CustomException):
    """
    Base not exist exception
    """


class UserNotExist(NotExist):
    """User not exist exception"""
