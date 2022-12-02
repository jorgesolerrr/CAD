import json
from os import getcwd
from .moodle_conn import Moodle
from .moodle_conn import User, Category, Course, Enroll
from .tools import lazy
import pandas as pd
from .core import CAD_Courses, CAD_Students


class CAD:
    def __init__(self, url: str, token: str, courseTime : str) -> None:
        moodle = Moodle(url, token)
        self._IUserMoodle = moodle.user
        self._ICourseMoodle = moodle.course
        self._ICategoryMoodle = moodle.category
        self._IEnrollMoodle = moodle.enroll
        self.courseTime = courseTime
        self.courses = CAD_Courses().GetCourses

    def _getCourseID(self, course):
        period = self.courses[course]["period"]
        course_idnumber = f"{course}-{period}_{self.courseTime}"
        response_course = self._ICourseMoodle.get_course_by_idnumber(course_idnumber)
        return response_course["courses"][0]["id"]

    @property
    @lazy
    def GetCADStudents(self) -> CAD_Students:
        return CAD_Students(self._IUserMoodle, self._ICourseMoodle)

    def EnrollStudentsInCAD(self, path: str):
        """Method for masive enrollment

        Args:
            path (str): path of current excel data
        Returns:
            dict: _description_
        """
        try:
            students_data = pd.read_excel(path, sheet_name="CAD")
        except Exception as e:
            raise (e)
        for index in students_data.index:
            try:
                username = students_data["CI"][index]
                firstLast_name = students_data["Nombre_Apellidos"][index].split()
            except Exception as e:
                raise (e)
            lastname = " ".join([firstLast_name[i] for i in range(2)])
            firstname = " ".join(
                [firstLast_name[i] for i in range(2, len(firstLast_name))]
            )
            newUser = User(
                username=username, firstname=firstname, lastname=lastname, email=None
            )
            try:
                response = self._IUserMoodle.create_user(newUser)
            except Exception as e:
                raise (e)
        return "success"

    def CreateCADCourses(self):
        """Method to create el distance learning course

        Args:
            courseTime (str): time of current course, like "2022-2023"
        """
        periods = ["1", "2"]

        
        for period in periods:
            newCategory = Category(
                name=f"CAD-{period}_{courseTime}", idnumber=f"CAD-{period}_{self.courseTime}"
            )
            cat_response = self._ICategoryMoodle.create_category(newCategory)
            try:
                for key in self.courses.keys():
                    if self.courses[key]["period"] == period:
                        newCourse = Course(
                            shortname=f"{key}_{self.courseTime}",
                            categoryid=cat_response[0]["id"],
                            fullname=self.courses[key]["name"] + "_" + self.courseTime,
                            idnumber=key + "-" + period + "_" + self.courseTime,
                        )
                        course_response = self._ICourseMoodle.create_course(newCourse)
                        group = self._ICourseMoodle.create_course_group(
                            course_response[0]["id"], f"{key}_{self.courseTime}"
                        )
            except Exception as e:
                raise e
        return "success"

    def EnrollStudentInCourse(self, fullname: str, course: str):
        courseID = self._getCourseID(course)
        newEnroll = Enroll(
            userID= self.GetCADStudents.GetStudents[fullname],
            courseID= courseID,
        )
        try:
            response = self._IEnrollMoodle.enroll_user_in_course(newEnroll)
        except Exception as e:
            raise e
        return "success"
    
    def GetStudentsFromCourse(self, course : str):
        courseID = self._getCourseID(course)
        return self._ICourseMoodle.get_enrolled_users_course_ByID(courseID)
    
    def ApproveStudent(self, fullnames : list, course : str):
        courseID = self._getCourseID(course)
        return self.GetCADStudents.ApproveStudentsInCOurse(fullnames, courseID)