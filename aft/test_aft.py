from __future__ import print_function

import unittest
from typing import Any, List, Optional

from ddt import data, ddt, unpack

from aft import aft
from aft.test_functions import Example


@ddt
class TestGrift(unittest.TestCase):

    @data(("add_one", [1], 2, "Test getting a single function"),
          ("Example.add_some_stuff", [Example(1, 2, "sum is:"), 1, 2],
           "sum is: 6", "Test getting a method from a class")
          )
    @unpack
    def test_get_function(self,
                          function_name,  # type: str
                          args,  # type: List[Any]
                          expected,  # type: Any
                          test_description,   # type:  str
                          ):
        """Tests that the correct functions are obtained programatically"""
        file_name = "test_functions"
        func = aft.get_function(file_name, function_name)
        result = func(*args)
        self.assertTrue(result == expected, test_description)

    @data(
          ("Example.add_some_stuff", Example(1, 2.0, "sum is:"), [1, 2],
           "sum is: 6.0", "Test applying arguments to a nested function"),
          ("Example.add_one_only_int_no_deps", Example(1, 2.0, "3"), [1],
           2, "Test applying arguments to a nested function no dependencies")
          )
    @unpack
    def test_class_func_app(self,
                            function_name,  # type:  str
                            class_instance,  # type: Any
                            args,  # type: List[Any]
                            expected,  # type: Any
                            test_description,  # type: str
                            ):
        file_name = "test_functions"
        func = aft.get_function(file_name, function_name)
        result = aft.class_func_app(class_instance, func, args)
        self.assertTrue(result == expected, test_description)

    @data(
          ("add_one_only_int", None, ["'int'"],
           "Test simple single input function with single type"),
          ("add_two_only_int", None, ["'int', 'int'"],
           "Test multi input function with single types"),
          ("add_one_multi_type", None, ["'int'", "'float'"],
           "Test single input function with multi types"),
          ("add_two_multi_type", None, ["'int', 'int'", "'int', 'float'",
                                        "'float', 'int'", "'float', 'float'",
                                        "'string', 'string'"],
           "Test multi input function with multi types"),
          ("Example.add_one_only_int_no_deps", Example(1, 2.0, "3"), ["'int'"],
           "Test method in class with no dependencies and single type"),
          ("Example.add_two_multi_type", Example(1, 2.0, 3),
           ["'int', 'int'", "'int', 'float'",
            "'float', 'int'", "'float', 'float'"],
           "Test method in class with multi types and dependencies"),
          ("Example.add_two_multi_type", Example(1, 2.0, "3"),
           [],
           "Test method in class with dependencies no feasable types"),
          ("add_one_only_int_default", None, ["'int'"],
           "test default parameters")
          )
    @unpack
    def test_fuzz_example_success(self,
                                  function_name,  # type: str
                                  class_instance,  # type: Optional[Any]
                                  expected,  # type: List[str]
                                  test_description,  # type: str
                                  ):
        output = aft.fuzz_example("test_functions",
                                  function_name,
                                  class_instance=class_instance)
        success_type_list = list(output["results"]["successes"].keys())
        self.assertListEqual(sorted(success_type_list),
                             sorted(expected),
                             test_description)

    @data(("add_one", ["x"], ["int"], ["def add_one(x: int) -> Any"],
           "Test simple single argument case"),
          ("add_two", ["x", "y"], ["int, str"],
           ["def add_two(x: int, y: str) -> Any"],
           "Test simple multi argument case"),
          ("add_two", ["x", "y"], ["int, str", "str, int"],
           ["def add_two(x: int, y: str) -> Any",
            "def add_two(x: str, y: int) -> Any"],
           "Test multi argument case multi string")
          )
    @unpack
    def test_generate_mypy_stub_string(self,
                                       function_name,  # type: str
                                       arg_names,  # type: List[str]
                                       arg_types,  # type: List[str]
                                       expected,  # type: str
                                       test_description,  # type: str
                                       ):
        function_json = {"function_to_type": function_name,
                         "arg_names": arg_names,
                         "results": {"successes": {k: [1] for k in arg_types}}
                         }

        function_string = aft.generate_mypy_stub_strings(function_json)

        self.assertEqual(function_string, expected, test_description)


if __name__ == "__main__":
    unittest.main()
