import json
from os import getcwd
from ..tools import lazy


class CAD_Courses:
    def __init__(self):
        with open(getcwd() + "\\resources\\courses.json") as _json:
            courses_json = json.load(_json)
            _json.close()
            periods = ["1", "2"]
            self.courses = {}
        for period in periods:
            for course in courses_json[period]:
                course_properties = {
                    "name" : course["name"],
                    "period" : period,
                    "precedence" : course["precedence"]
                }
                self.courses.update({course["shortname"] : course_properties})
 
    @property
    @lazy
    def GetCourses(self):
        return self.courses

    def GetCoursesInPeriod(self, period : str):
        result = {}
        for key in self.courses.keys():
            if self.courses[key]["period"] == period:
                result.update({key : self.courses[key]})
        return result

    @property
    @lazy
    def GetCoursesWithOutPrecedence(self):
        result = {}
        for key in self.courses.keys():
            if len(self.courses[key]["precedence"]) == 0:
                result.update({key : self.courses[key]})
        return result

    def GetPrecedence(self, shortname : str):
        return self.courses[shortname]["precedence"]

