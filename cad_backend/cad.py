from moodle_conn.moodle import Moodle
from core.schemas import *
import pandas as pd

class CAD:
    
    def __init__(self, url : str, token : str) -> None:
        moodle = Moodle(url, token)
        self.__user = moodle.user
        self.__course = moodle.course
        self.__category = moodle.category    
    
    def EnrollStudents(self, path : str):
        """Method for masive enrollment

        Args:
            path (str): path of current excel data 
        Returns:
            dict: _description_
        """
        try:
            students_data = pd.read_excel(path, sheet_name = "CAD")
        except Exception as e:
            raise(e)
        for index in students_data.index:
            try:
                username = students_data[index]["CI"]
                firstLast_name = students_data[index]["Nombre_Apellidos"].split()
            except Exception as e:
                raise(e)
            lastname = " ".join([firstLast_name[i] for i in range(2)])
            firstname = " ".join([firstLast_name[i] for i in range(2, len(firstLast_name))])
            newUser = User(
                username = username, 
                firstname = firstname, 
                lastname= lastname
            )
            try:
                response = self.__user.create_user(newUser)
            except Exception as e:
                raise (e)
        return "success"

    def CreateCAD(self, period : str, courseTime : str):
        newCategory = Category(name = f"CAD_{period}_{courseTime}", idnumber = f"CAD_{period}_{courseTime}")
        response = self.__category.create_category(newCategory)
        
    




