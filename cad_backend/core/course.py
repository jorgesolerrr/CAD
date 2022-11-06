from dataclasses import dataclass
from moodle_conn.moodle import Moodle 
from core.schemas import *


class BaseCourse(Moodle):
    def create_course(course : Course):
        course.