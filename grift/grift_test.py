import os
import unittest
from typing import Any, Dict, List, Optional, Set

from ddt import data, ddt, unpack

from grift import get_function, fuzz_example
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
          # ("Example.add_one_only_int_no_deps", Example(1, 2, 3), ["'int'"],
          #  "Test method in class with no dependencies and single type"),
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
        print(output['results']["successes"])
        self.assertListEqual(success_type_list, expected, test_description)


if __name__ == "__main__":
    unittest.main()
