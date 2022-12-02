from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username : str
    firstname : str
    lastname : str
    email : Optional[str]

@dataclass
class Course :
    shortname: str
    categoryid: int
    fullname: str
    idnumber : str

@dataclass
class Category:
    name : str
    idnumber : str
    parent: Optional[int] = 0

@dataclass
class Enroll:
    userID : int
    courseID : int