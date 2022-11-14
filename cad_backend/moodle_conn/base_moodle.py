import json
from requests import Session
from requests.exceptions import RequestException
from ..tools.helper import make_params
from ..tools.exceptions import *

class BaseMoodle:
    """ Base class for moodle communication

        Init :
            URL : url of current moodle
            TOKEN : token of moodle webservice account 
    """
    
    session : Session = Session()
    
    def __init__(self, url : str, token : str):
        self.URL = url
        self.TOKEN = token
        
    
    def get(self, wsfunction: str, **kwargs):
        params = make_params(self.TOKEN, wsfunction)
        params.update(kwargs)
        try:
            response = self.session.get(self.URL, params=params)
        except RequestException as e:
            raise NetworkMoodleException(e)
        if response.ok:
            data = json.loads(response.text)
            if "exception" in data or "errorcode" in data:
                raise MoodleException(**data)
            return data
        return response.text
    
    def post(self, wsfunction : str, **kwargs):
        params = make_params(self.TOKEN, wsfunction)
        try:
            response = self.session.post(self.URL, data = kwargs, params=params)
        except RequestException as e:
            raise NetworkMoodleException(e)
        if not response.ok or not response.text:
            raise EmptyResponseException()
        if response.ok :
            data = json.loads(response.text)
            if "exception" in data or "errorcode" in data:
                raise MoodleException(**data)
            return data
        return response.text
        