"""
This file holds instances of defined fuzz generators.  These methods are used
to fuzz the python code.
"""

import random
from typing import Any, List, Tuple

# todo iterative generation

Example = List[Tuple[str, Any]]


def get_dummy():
    # type: () -> Example
    return [("dummy one", 1)]


def get_ints():
    # type: () -> Example
    # todo control how many you want to try
    ints = [1, 0, -1]
    ints += [random.randint(-1000, 1000) for _ in range(10)]
    return list(map(lambda x: ("int", x), ints))


def get_floats():
    # type: () -> Example
    floats = [-1.5, 0.0, 1.3]
    floats += [random.random() * 100 for _ in range(10)]
    return list(map(lambda x: ("float", x), floats))


def get_bools():
    # type: () -> Example
    bools = [True, False]
    return list(map(lambda x: ("bool", x), bools))


# todo, random strings & edge case strings (for type refinement)
def get_strings():
    # type: () -> Example
    strings = ["a", "", "빵", "الكلب", "🦝",
               "\"Life is rolling on, and it's all very exciting\""]
    return list(map(lambda x: ("str", x), strings))


def make_identical_lists(x, type_annotation):
    # type: (Any, str) -> Example
    lists = [[x], [x] * 2, [x] * 5, [x] * 50, []]
    full_type = "List[" + type_annotation + "]"
    return list(map(lambda v: (full_type, v), lists))


def get_int_list():
    # type: () -> Example
    return make_identical_lists(1, "int")


def get_float_list():
    # type: () -> Example
    return make_identical_lists(1.0, "float")


def get_string_list():
    # type: () -> Example
    return make_identical_lists("trust your silent captain", "string")


def get_numpy_arrays():
    # type: () -> Example
    try:
        import numpy as np
        arrs = [np.array([1]), np.array([1, 2, 3]), np.array([[1, 2], [3, 4]])]
        return list(map(lambda x: ("np.array", x), arrs))
    except ImportError:
        return []

# tuples, nested lists, multiple arguments


def get_instances():
    # type: () -> Example
    return get_ints() + get_floats() + get_bools() \
           + get_strings() + get_int_list() + get_float_list() + \
           get_string_list() + get_numpy_arrays()
