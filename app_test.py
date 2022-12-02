from os import getenv
# from cad_backend.moodle_conn.moodle import Moodle
# from cad_backend.core.core_course.schemas import Course
from cad_backend import CAD

url = getenv("MOODLE_URL")
token = getenv("MOODLE_TOKEN")

cad = CAD(url, token, "2022-2023")

students = cad.GetCADStudents
# courses = ["POPTUR", "MSAE", "F", "CF", "DE"]
# for c in courses:
#     response = cad.EnrollStudentInCourse("Abraham de Jesús Martínez Fortes", c)
#     result = cad.ApproveStudent(["Abraham de Jesús Martínez Fortes"], c)

courses = students.GetNextCoursesToEnroll("Abraham de Jesús Martínez Fortes")
print(courses)
#TODO move to login method of moodle_conn class
# import requests
# import re

# login = 12345678
# passwd = 'password'

# r = requests.get("http://localhost/login/index.php")
# cookie = r.cookies.get_dict()
# pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
# token = re.findall(pattern, r.text)
# token = re.findall("\w{32}", token[0])
# payload = {'username': "admin", 'password': "Relos281000*", 'anchor': '', 'logintoken': token[0]}
# r = requests.post("http://localhost/login/index.php", cookies=cookie, data=payload)



