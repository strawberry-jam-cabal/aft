import os
import unittest
from typing import Any, Dict, List, Optional, Set

from ddt import data, ddt, unpack

from grift import get_function, fuzz_example, class_func_app
from test_functions import Example


@ddt
class TestGrift(unittest.TestCase):

    @data(("add_one", [1], 2, "Test getting a single function"),
          ("Example.add_some_stuff", [Example(1, 2, "sum is:"), 1, 2],
           "sum is: 6", "Test getting a method from a class")
          )
    @unpack
    def test_get_function(self,
                          function_name: str,
                          args: List[Any],
                          expected: Any,
                          test_description: str
                          ) -> None:
        """Tests that the correct functions are obtained programatically"""
        file_name = "test_functions"
        func = get_function(file_name, function_name)
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
                            function_name: str,
                            class_instance: Any,
                            args: List[Any],
                            expected: Any,
                            test_description: str
                            ) -> None:
        file_name = "test_functions"
        func = get_function(file_name, function_name)
        result = class_func_app(class_instance, func, args)
        print(result)
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
          )
    @unpack
    def test_fuzz_example_success(self,
                                  function_name: str,
                                  class_instance: Optional[Any],
                                  expected: List[str],
                                  test_description: str
                                  ) -> None:
        output = fuzz_example("test_functions",
                              function_name,
                              class_instance=class_instance)
        success_type_list = list(output["results"]["successes"].keys())
        self.assertListEqual(success_type_list, expected, test_description)


if __name__ == "__main__":
    unittest.main()
