import os
import sys
from models.member import Member

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

Member.add_member(
    name = "Ozge",
    email = "ozgeseven56@gmail.com",
    password = "ozgemels",
    role_id=1
)
