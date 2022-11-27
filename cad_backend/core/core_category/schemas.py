from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    name : str
    idnumber : str
    parent : Optional[int]