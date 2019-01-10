import os
import unittest
from typing import Any, List, Optional, Set

from ddt import data, ddt, unpack

from grift import get_function
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


if __name__ == "__main__":
    unittest.main()
