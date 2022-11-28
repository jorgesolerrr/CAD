from .base_moodle import BaseMoodle
from ..core.core_user.user import BaseUser
from ..core.core_category.category import BaseCategory
from ..core.core_course.course import BaseCourse
from ..tools.decorators import lazy

class Moodle(BaseMoodle):
    
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
    
    

