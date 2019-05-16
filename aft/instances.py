"""
This file holds instances of defined fuzz generators.  These methods are used
to fuzz the python code.
"""

import numpy as np

# todo iterative generation


def get_dummy():
    return [("dummy one", 1)]


def get_ints():
    # todo control how many you want to try
    ints = [1, 0, -1]
    ints += np.random.randint(-1000, 1000, 10).tolist()
    return list(map(lambda x: ("int", x), ints))


def get_floats():
    floats = [-1.5, 0.0, 1.3]
    floats += (np.random.rand(10) * 100).tolist()
    return list(map(lambda x: ("float", x), floats))


def get_bools():
    bools = [True, False]
    return list(map(lambda x: ("bool", x), bools))


# todo, random strings & edge case strings (for type refinement)
def get_strings():
    strings = ["\"a\"", "\"\"",
               "\"life is rolling on, and it's all very exciting\""]
    return list(map(lambda x: ("string", x), strings))


def make_identical_lists(x, type_annotation):
    lists = [[x], [x] * 2, [x] * 5, [x] * 50, []]
    full_type = "[" + type_annotation + "]"
    return list(map(lambda v: (full_type, v), lists))


def get_int_list():
    return make_identical_lists(1, "int")


def get_float_list():
    return make_identical_lists(1.0, "float")


def get_string_list():
    return make_identical_lists("trust your silent captain", "string")


def get_numpy_arrays():
    arrs = [np.array([1]), np.array([1, 2, 3]), np.array([[1, 2], [3, 4]])]
    return list(map(lambda x: ("np.array", x), arrs))

# tuples, nested lists, multiple arguments


def get_instances():
    return get_ints() + get_floats() + get_bools() \
           + get_strings() + get_int_list() + get_float_list() + \
           get_string_list() + get_numpy_arrays()
