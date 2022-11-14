from .base_moodle import BaseMoodle
from ..core.core_course.course import BaseCourse
from ..tools.decorators import lazy
class Moodle(BaseMoodle):
    
    def __init__(self, url : str, token : str):
        super(Moodle, self).__init__(url, token)
    
    @property
    @lazy
    def course(self) -> BaseCourse:
        return BaseCourse(self)
    

