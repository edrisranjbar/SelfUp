from models.task import *
from models.category import *
from models.result import *
from models.user import *

def create_all_tables():
    Task.create_table()
    Result.create_table()
    Category.create_table()
    User.create_table()