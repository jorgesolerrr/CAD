from ..tools import lazy
from .cad_courses import CAD_Courses

class CAD_Students: 
    def __init__(self, baseUser, baseCourse):
        self._IUserMoodle = baseUser
        self._ICourseMoodle = baseCourse
        response = baseUser.get_all_users()
        self.students = {}
        for user in response["users"]:
            if user["id"] == 2 : continue
            self.students.update({user["fullname"] : user["id"]})

    @property
    @lazy
    def GetStudents(self):
        return self.students

    def ApproveStudentsInCOurse(self, fullname : list, courseID):
        group = self._ICourseMoodle.get_course_group(courseID)
        for name in fullname:
            try:
                response = self._IUserMoodle.add_user_to_group(self.students[name], group[0]["id"])
            except Exception as e:
                raise e
        return "success"

    def GetApprovedCourses(self, fullname : str) -> set:
        result = []
        try:
            groups = self._IUserMoodle.get_user_groups(self.students[fullname])
            for group in groups["groups"]:
                result.append(group["name"])
        except Exception as e:
            raise e
        return set(result)
    
    def GetMissingCoursesFromStudent(self, approved : set):
        all_courses = CAD_Courses().GetCourses
        if len(approved) == 0:
            return all_courses        
        result = {}
        difference =  all_courses.keys() - approved
        for key in difference:
            result.update({key : all_courses[key]})
        
        return result

    def GetNextCoursesToEnroll(self, fullname : str) :
        approved_set = self.GetApprovedCourses(fullname)
        approved_set.add("")
        missing = self.GetMissingCoursesFromStudent(approved_set)
        result = {}
        for key in missing.keys():
            i = 0
            for prec in missing[key]["precedence"]:
                if prec in approved_set:
                    i += 1
            if i == len(missing[key]["precedence"]):
                result.update({key : missing[key]})

        return result

        

        

        
