import random
import string
import uuid


def random_char(y):
    """
    returns y number of uppercase random characters
    """
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))


def new_guid():
    """
    returns a unique id (uuid)
    """
    new_id = str(uuid.uuid4())
    return new_id