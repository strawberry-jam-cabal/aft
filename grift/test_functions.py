def add_one(a):
    return a + 1


class Example(object):

    def __init__(self, a: int, b: float, c: str):
        self.a = a
        self.b = b
        self.c = c

    def add_some_stuff(self, x: int, y: int) -> str:
        return f"{self.c} {x + y + self.a + self.b}"