
from ..core_moodle import MoodleCore
from ..schemas import Course



class BaseCourse(MoodleCore):

    def create_course(self, course : Course):
        data = {
            "courses[0][fullname]" : course.fullname,
            "courses[0][shortname]" : course.shortname,
            "courses[0][categoryid]" : course.categoryid,
            "courses[0][idnumber]" : course.idnumber
        }
        return self.moodle._post("core_course_create_courses", **data)
    
    def get_course_by_shortname(self, name : str):
        params = {
            "field" : "shortname",
            "value" : name
        }
        return self._get("core_course_get_courses_by_field", **params)
    
    def get_course_by_idnumber(self, idnumber : str):
        params = {
            "field" : "idnumber",
            "value" : idnumber
        }
        return self.moodle._get("core_course_get_courses_by_field", **params)

    def get_enrolled_users_course_ByID(self, courseID : int):
        params = {
            "courseid" : courseID,
            "options[0][name]" : "userfields",
            "options[0][value]" : "username, fullname, lastname, email"
        }
        return self.moodle._get("core_enrol_get_enrolled_users", **params)

    def get_all_courses(self, courseTime, period : str = ""):
        params = {
            "criterianame" : "search",
            "criteriavalue" : f"{period}_{courseTime}" if period != "" else courseTime
        }
        return self.moodle._get("core_course_search_courses", **params)
    
    def create_course_group(self, courseID : int, name : str):
        data = {
            "groups[0][courseid]" : courseID,
            "groups[0][name]" : name,
            "groups[0][description]" : f"Estudiantes que vencieron el curso de {name}"
        }
        return self.moodle._post("core_group_create_groups", **data)
    
    def get_course_group(self, courseID : int):
        params = {
            "courseid" : courseID,
        }
        return self.moodle._get("core_group_get_course_groups", **params)
    