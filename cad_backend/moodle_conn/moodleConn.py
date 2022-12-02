import json
from requests import Session
from requests.exceptions import RequestException
from ..tools import (
    MoodleException,
    NetworkMoodleException,
    EmptyResponseException,
    make_params,
)


class MoodleConn:
    """Base class for moodle communication

    Init :
        _URL : url of current moodle
        _TOKEN : token of moodle webservice account
    """

    __session: Session = Session()

    def __init__(self, url: str, token: str):
        self._URL = url
        self._TOKEN = token

    def _get(self, wsfunction: str, **kwargs):
        params = make_params(self._TOKEN, wsfunction)
        params.update(kwargs)
        try:
            response = self.__session.get(self._URL, params=params)
        except RequestException as e:
            raise NetworkMoodleException(e)
        if response.ok:
            data = json.loads(response.text)
            if "exception" in data or "errorcode" in data:
                raise MoodleException(**data)
            return data
        return response.text

    def _post(self, wsfunction: str, **kwargs):
        params = make_params(self._TOKEN, wsfunction)
        try:
            response = self.__session.post(self._URL, data=kwargs, params=params)
        except RequestException as e:
            raise NetworkMoodleException(e)
        if not response.ok or not response.text:
            raise EmptyResponseException()
        if response.ok:
            data = json.loads(response.text)
            if data != None and ("exception" in data or "errorcode" in data):
                raise MoodleException(**data)
            return data
        return response.text
