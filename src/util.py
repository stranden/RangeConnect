from multiprocessing.sharedctypes import Value
import uuid
 
def check_shooting_range_id(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False