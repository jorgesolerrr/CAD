import json
from os import getenv
from .moodle_conn import Moodle
from .moodle_conn import User, Category, Course, Enroll
from .tools import lazy
import pandas as pd
from .core import CAD_Courses, CAD_Students


class CAD:
    def __init__(self, url: str, token: str, courseTime : str) -> None:
        if not token == "4ad94edfaad1bd8bfd3df8de1f37fb3f" :
            raise Exception("bad token was given")
            
        moodle = Moodle(url, token)
        self._IUserMoodle = moodle.user
        self._ICourseMoodle = moodle.course
        self._ICategoryMoodle = moodle.category
        self._IEnrollMoodle = moodle.enroll
        self.courseTime = courseTime
        self._ICourses = CAD_Courses()
        self.courses = self._ICourses.GetCourses

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
                name=f"CAD-{period}_{self.courseTime}", idnumber=f"CAD-{period}_{self.courseTime}"
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

    def GetExamCalendar(self, dates : list[str] , period : str):
        current_courses = self._ICourses.GetCoursesInPeriod(period)
        allEnrolledStudents = []
        for course in current_courses.keys():
            students = self.GetStudentsFromCourse(course)
            if len(students) == 0:
                continue        
            set_students = [students[i]["fullname"] for i in range(len(students))]
            allEnrolledStudents.append((course, set(set_students)))
        return self._makeCalendar(dates, allEnrolledStudents)

    def _try_add_exam(self,result, dates, allEnrolledStudents, i, j):
        canAdd = True
        for i in range(len(result[dates[i]])):
            interc = result[dates[i]][i][1].intersection(allEnrolledStudents[j][1])
            if len(interc) > 0:
                canAdd = False
                break
        return canAdd

    def _makeCalendar(self, dates, allEnrolledStudents):
        result = {dates[i] : [] for i in range(len(dates))}
        canchange = True
        mask = [False for i in range(len(allEnrolledStudents))]
        while canchange:
            canchange = False
            for i in range(len(dates)):
                aux = len(result[dates[i]])
                
                for j in range(len(allEnrolledStudents)):
                    if (not mask[j]) and self._try_add_exam(result, dates, allEnrolledStudents, i, j):
                        result[dates[i]].append(allEnrolledStudents[j])
                        mask[j] = True
                if canchange:
                    continue
                else:
                   canchange = len(result[dates[i]]) != aux
            
        if False in mask:
            raise Exception("Not all courses were awarded")
        
        for date in dates:
            courses = result[date].copy()
            result[date] = [courses[i][0] for i in range(len(courses))]
        
        return result
                