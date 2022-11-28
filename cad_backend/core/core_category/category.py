from ...moodle_conn.moodle import Moodle 
from ..schemas import Category

class BaseCategory(Moodle):

    def create_category(self, category : Category):
        data = {
            "categories[0][name]" : category.name,
            "categories[0][parent]" : category.parent,
            "categories[0][idnumber]" : category.idnumber
        }
        return self._post("core_course_create_categories", **data)