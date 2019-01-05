import unittest
from typing import Any, List, Optional, Set

from ddt import data, ddt, unpack

from grift.grift import get_function


@ddt
class TextToolsTest(unittest.TestCase):

    @data(("Example.add_some_stuff", "Test getting a single function"),
          ("add_one", "Test getting a method from a class")
          )
    @unpack
    def test_get_function(self,
                          function_name: str,
                          test_description: str
                          ) -> None:
        """Tests that the correct functions are obtained programatically"""
        file_name = "test_functions.py"
        func = get_function(file_name, function_name)



if __name__ == "__main__":
    unittest.main()
