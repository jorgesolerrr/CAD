from .moodleConn import MoodleConn
from .base import BaseCategory, BaseUser, BaseCourse, BaseEnroll
from ..tools import lazy
class Moodle(MoodleConn):
    
    def __init__(self, url : str, token : str):
        super().__init__(url, token)
    
    @property
    @lazy
    def course(self) -> BaseCourse:
        return BaseCourse(self)
        
    
    @property
    @lazy
    def user(self) -> BaseUser:
        return BaseUser(self)
    
    @property
    @lazy
    def category(self) -> BaseCategory:
         return BaseCategory(self)
    
    @property
    @lazy
    def enroll(self) -> BaseEnroll:
        return BaseEnroll(self)
    
    

