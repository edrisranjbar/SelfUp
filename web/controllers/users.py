from models.task import *
from models.category import *
from models.result import *
from models.user import *


def check_user_exists(email, password):
    return User.exists(email, password)

def add_new_user(name, email, password):
    add_user_status = User.add(name, email, password)
    return add_user_status