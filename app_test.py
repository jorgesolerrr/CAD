from os import getenv
from cad_backend.moodle_conn.moodle import Moodle
from cad_backend.core.core_course.schemas import Course

url = getenv("MOODLE_URL")
token = getenv("MOODLE_TOKEN")

mymoodle = Moodle(url, token)

moodle_course = mymoodle.course



response = moodle_course.create_course(
                                    Course(  
                                            shortname = "curso_prueba_01", 
                                            categoryid = 1, 
                                            fullname = "curso_prueba_01", 
                                            idnumber = "prueba_1"
                                        )
                                )

print(response)

