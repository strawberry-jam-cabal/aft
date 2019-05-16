def add_one(a):
    return a + 1


def add_one_only_int(a):
    if type(a) != int:
        raise TypeError()
    else:
        return a + 1


def add_two_only_int(a, b):
    if type(a) != int or type(b) != int:
        raise TypeError()
    else:
        return a + b


def add_one_multi_type(a):
    if type(a) not in [int, str, float]:
        raise TypeError()
    else:
        return a + 1


def add_two_multi_type(a, b):
    types = [int, str, float]
    if type(a) not in types or type(b) not in types:
        raise TypeError()
    else:
        return a + b


def add_one_only_int_default(a, b=3, c=4):
    if type(a) != int:
        raise TypeError()
    else:
        return a + b + c + 1


class Example(object):

    def __init__(self, a, b, c):
        # type: (int, float, str) -> None
        self.a = a
        self.b = b
        self.c = c

    def add_some_stuff(self, x, y):
        # type: (int, int) -> str
        answer = x + y + self.a + self.b
        return "{} {}".format(self.c, answer)

    def add_one_only_int_no_deps(self, a):
        if type(a) != int:
            raise TypeError()
        else:
            return a + 1

    def add_two_multi_type(self, a, b):
        types = [int, str, float]
        if type(a) not in types or type(b) not in types:
            raise TypeError()
        else:
            return self.c + a + b + self.a + self.b

