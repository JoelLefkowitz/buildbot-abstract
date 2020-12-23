from names import get_first_name

from .exceptions import MaxUniqueNameAttempts


def get_unique_name(taken_names, max_tries=10):
    for i in range(max_tries):
        name = get_first_name()

        if name not in taken_names:
            return name

    raise MaxUniqueNameAttempts(max_tries)
