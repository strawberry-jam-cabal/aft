from lop import *

def test_add_result():
    acc = []        
    add_result(acc, "int", 1) 
    assert acc == [("int", 1)]
    add_result(acc, "int", 2)  
    assert acc == [("int", 1)]
    add_result(acc, "string", "yo") 
    assert acc == [("int", 1), ("string", "yo")]