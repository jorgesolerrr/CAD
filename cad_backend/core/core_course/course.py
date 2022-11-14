from ...moodle_conn.base_moodle import BaseMoodle 
from .schemas import Course



class BaseCourse(BaseMoodle):

    def __init__(self, moodle : BaseMoodle):
        super().__init__(moodle.URL, moodle.TOKEN)
        

    def create_course(self, course : Course):
        data = {
            "courses[0][fullname]" : course.fullname,
            "courses[0][shortname]" : course.shortname,
            "courses[0][categoryid]" : course.categoryid,
            "courses[0][idnumber]" : course.idnumber
        }
        return self.post("core_course_create_courses", **data)
    
    def get_course_by_shortname(self, name : str):
        params = {
            "field" : "shortname",
            "value" : name
        }
        return self.get("core_course_get_courses_by_field", **params)
    
    def get_course_by_idnumber(self, idnumber : str):
        params = {
            "field" : "shortname",
            "value" : idnumber
        }
        return self.get("core_course_get_courses_by_field", **params)

    def get_enrolled_users_course_ByID(self, courseID : int):
        params = {
            "courseid" : courseID
        }
        return self.get("core_enrol_get_enrolled_users", **params)