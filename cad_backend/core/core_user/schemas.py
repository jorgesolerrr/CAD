from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username : str
    firstname : str
    lastname : str
    email : Optional[str]


