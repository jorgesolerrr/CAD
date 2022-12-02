from ..core_moodle import MoodleCore 
from ..schemas import Category

class BaseCategory(MoodleCore):


    def create_category(self, category : Category):
        data = {
            "categories[0][name]" : category.name,
            "categories[0][parent]" : category.parent,
            "categories[0][idnumber]" : category.idnumber
        }
        try: 
            response = self.moodle._post("core_course_create_categories", **data)
        except:
            return self.search_category(category.idnumber)
        return response
    
    def search_category(self, idnumber : str) :
        params = {
            "criteria[0][key]" : "idnumber",
            "criteria[0][value]" : idnumber,
            "addsubcategories" : 0
        }
        return self.moodle._get("core_course_get_categories", **params)
        