# from cad_backend.moodle_conn.moodle import Moodle
# from cad_backend.core.core_course.schemas import Course
from cad_frontend import MainApp
# from cad_backend import CAD
app = MainApp()
app.run()


# cad = CAD("http://localhost/webservice/rest/server.php", "4ad94edfaad1bd8bfd3df8de1f37fb3f", "2022-2023")

# print(cad.GetExamCalendar(["1","2","3","4"], "1"))
# # response = cad.CreateCADCourses()
# students = cad.GetCADStudents
# courses = ["POPTUR", "MSAE", "F", "CF", "DE"]
# for c in courses:
#     response = cad.EnrollStudentInCourse("Abraham de Jesús Martínez Fortes", c)
#     result = cad.ApproveStudent(["Abraham de Jesús Martínez Fortes"], c)

# courses = students.GetNextCoursesToEnroll("Abraham de Jesús Martínez Fortes")
# print(courses)


