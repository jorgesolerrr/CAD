from moodle_conn.moodle import Moodle 
from core.schemas import *


class BaseCourse(Moodle):
    def create_course(self, course : Course):
        data = {
            "courses[0][fullname]" : course.fullname,
            "courses[0][shortname]" : course.shortname,
            "courses[0][categoryid]" : course.categoryid,
            "courses[0][idnumber]" : course.idnumber
        }
        