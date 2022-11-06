from typing import Optional
from requests.exceptions import RequestException

class BaseException(Exception):
    """
    Base class for all exceptions

    """
    pass

class MoodleException(BaseException):
    def __init__(self, exception : str = "", errorcode : str = "", message : str = ""):
        BaseException.__init__(self, exception or errorcode or message)
    
class EmptyResponseException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "Empty response from server!")

class NetworkMoodleException(BaseException):
    """Moodle wrapper for network related network error"""
    def __init__(self, exception : Optional[RequestException]):
        BaseException.__init__(self, "A Network error occurred: " + exception.strerror)