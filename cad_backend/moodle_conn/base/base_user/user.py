
from ..core_moodle import MoodleCore 
from ..schemas import User

class BaseUser(MoodleCore):

    def create_user(self, user : User):
        data = {
            "users[0][createpassword]" : 1,  
            "users[0][username]" : str(user.username),
            "users[0][password]" : "Cad.2020",
            "users[0][firstname]" : user.firstname,
            "users[0][lastname]" : user.lastname,
            "users[0][email]" : user.email if user.email is not None else f"{str(user.username)}@email.com",
        }
        try:
            return self.moodle._post("core_user_create_users", **data)
        except:
            return self.get_user_by_username(str(user.username))

    def get_user_by_username(self, username : str):
        params = {
            "field" : "username",
            "values[0]" : username
        }
        return self.moodle._get("core_user_get_users_by_field", **params)

    def get_courses_enrolled(self, userID : int):
        params = {
            "userid" : userID,
            "returnusercount" : 0
        }
        return self.moodle._get("core_enrol_get_users_courses", **params)

    def get_all_users(self):
        params = {
            "criteria[0][key]" : "",
            "criteria[0][value]" : ""
        }
        return self.moodle._get("core_user_get_users", **params)
    
    def add_user_to_group(self, userID : int, groupID : int):
        data = {
            "members[0][groupid]" : groupID,
            "members[0][userid]" : userID
        }
        return self.moodle._post("core_group_add_group_members", **data)
    
    def get_user_groups(self, userID : int):
        params = {
            "userid" : userID
        }
        return self.moodle._get("core_group_get_course_user_groups", **params)