from ...moodle_conn.moodle import  Moodle
from ...moodle_conn.base_moodle import BaseMoodle 
from .schemas import User

class BaseUser(Moodle):

    def create_user(self, user : User):
        data = {
            "users[0][username]" : user.username,
            "users[0][firstname]" : user.firstname,
            "users[0][lastname]" : user.lastname,
            "users[0][email]" : user.email if user.email is not "" else f"{user.firstname + user.lastname}@email.com",
            "users[0][createpassword]" : 1,  
            "users[0][password]" : "Cad.2020"
        }
        return self.post("core_user_create_users", **data)
    
    def get_users_by_username(self, username : str):
        params = {
            "field" : "username",
            "value" : username
        }
        return self.get("core_user_get_users_by_field", **params)

    def get_courses_enrolled(self, userID : int):
        params = {
            "userid" : userID,
            "returnusercount" : 0
        }
        return self.get("core_enrol_get_users_courses", **params)

    