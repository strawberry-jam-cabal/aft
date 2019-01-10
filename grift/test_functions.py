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


class Example(object):

    def __init__(self, a: int, b: float, c: str):
        self.a = a
        self.b = b
        self.c = c

    def add_some_stuff(self, x: int, y: int) -> str:
        return f"{self.c} {x + y + self.a + self.b}"
