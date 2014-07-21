import random
import string


def format_money(price):
    return "{:8.2f}".format(price)


def random_string_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
