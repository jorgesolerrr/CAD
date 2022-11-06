from dataclasses import dataclass
from typing import Optional

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
    parent: Optional[str]