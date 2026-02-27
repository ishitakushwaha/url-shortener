import random
import string

BASE62 = string.ascii_letters + string.digits

def generate_short_code(length=7):
    return "".join(random.choices(BASE62, k=length))
