from moodle_conn.base_moodle import BaseMoodle

class Moodle(BaseMoodle):
    
    def __init__(self, url : str, token : str):
        super(Moodle, self).__init__(url, token)
    
    
    