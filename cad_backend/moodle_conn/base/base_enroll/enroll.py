from ..core_moodle import MoodleCore
from ..schemas import Enroll

class BaseEnroll(MoodleCore):
    
    def enroll_user_in_course(self, enroll : Enroll):
        data = {
            "enrolments[0][roleid]" : 5,
            "enrolments[0][userid]" : enroll.userID,
            "enrolments[0][courseid]" : enroll.courseID
        }
        return self.moodle._post("enrol_manual_enrol_users", **data)
    
