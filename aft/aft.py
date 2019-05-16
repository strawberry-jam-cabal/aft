"""
AFT is Fuzzy Typing is a python type fuzzer which can be used to type check
python modules, files, and single functions.
"""
from __future__ import print_function

import os
import sys
from collections import defaultdict
from itertools import product, repeat
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

import click

from aft.instances import *

if sys.version_info[0] < 3:
    from inspect import getmembers, isclass, isfunction
    from funcsigs import signature, Parameter
else:
    from inspect import signature, Parameter, getmembers, isclass, isfunction

# Set the environment codec variables so that click is callable from python3
if 'linux' in sys.platform:
    os.environ['LC_AL'] = "C.UTF-8"
    os.environ['LANG'] = "C.UTF-8"
else:
    os.environ['LC_AL'] = "en_US.utf-8"
    os.environ['LANG'] = "en_US.utf-8"


# Define generic type variables
A = TypeVar("A")
B = TypeVar("B")
CLS = TypeVar("CLS")


@click.group()
def main():
    pass

    """
JSON SPEC

    [
        {
        function_to_type : addOnes
        arg_names : ["x", "y"]
        results :
            {
                successes:
                    {
                        string : ["a", "b"]
                        int : [1, -2]
                    }
                failures:
                    {
                        string : ["-a", "*b"]
                        int : [-1, 2]
                    }
            }
    ]
    """


def get_all_functions_in_module(module_name, module_str):
    # type: (Any, str) -> Any
    """Gets all classes and sub methods from a module
    """
    potential_classes = [(name, obj) for name, obj in getmembers(module_name) if
                         isclass(obj) and obj.__module__ == module_str]

    # TODO:: INheritance fucks us
    all_classes = [(name, obj, getmembers(obj, predicate=isfunction))
                   for name, obj in potential_classes]

    return all_classes


def generate_mypy_stub_strings(function_example_dict):
    # type: (Dict[str, Any]) -> List[str]
    """

    Args:
        function_example_dict:

    Returns:

    """
    stub_strings = []
    zipped_types = [zip(function_example_dict["arg_names"], k.split(", ")) for
                    k, _ in
                    function_example_dict["results"]["successes"].items()]

    # zipped_types = zip(function_example_dict["arg_names"],
    #                    function_example_dict["results"]["successes"])
    for args in zipped_types:
        stub_string = ["def ", function_example_dict["function_to_type"], "("]
        for arg_name, arg_type in args:
            stub_string.append(arg_name)
            stub_string.append(": ")
            stub_string.append(arg_type)
            stub_string.append(", ")

        stub_strings.append("".join(stub_string[:-1] + [") -> Any"]))

    return stub_strings


def generate_mypy_stub_file(json_types):
    # type: (Dict[str, Any]) -> None
    to_write = []
    for func in json_types:
        to_write.append("def ")
        to_write.append(function["function_to_type"])
        to_write.append("(")
        for arg_name, arg_type in zip(function["arg_names"], function["results"]["successes"]):
            to_write.append(arg_name)
            to_write.append(": ")
            to_write.append(arg_type)
            to_write.append(", ")
        to_write[:-2].append(") -> Any")
    print()


def print_thin_bar(width):
    print("-" * width)


def print_thick_bar(width):
    print("-" * width)


def default_print(json_obj, print_failures=False):
    # type: (Union[List[Any], Dict[Any, Any]], bool) -> Any
    for func in json_obj:
        indent = 40
        width = 80
        print_thick_bar(width)

        print(" "*(indent-2) + "TESTED\n" + str(func["function_to_type"]))
        results = func["results"]

        print("\n" + " "*(indent-3) + "SUCCESSES")

        print("-"*indent + "|" + "-"*(width-indent-1))
        print(" "*((indent//2)-2) + "type" + " "*((indent//2)-2) + "|" + "   " + "instance")
        print("-"*indent + "+" + "-" * (width - indent - 1))

        for types, insts in results["successes"].items():
            print(types.rjust(indent-1) + " | ", insts[0])

        if print_failures:

            print("\n\n" + " "*(indent-3) + "FAILURES")

            print("-"*indent + "+" + "-"*(width-indent-1))
            print(" "*((indent//2)-2) + "type" + " "*((indent//2)-2) + "|" + "   " + "instance")
            print("-"*indent + "+" + "-" * (width - indent - 1))

            for types, insts in results["failures"].items():
                print(types.rjust(indent-1) + " | ", insts[0])
            print_thick_bar(width)


def show_results(typeAccum):
    for (typeAnnotation, inst) in typeAccum:
        print(typeAnnotation + "|", inst)


@main.command("fuzz")
@click.argument("file-path")
@click.argument("function-name")
@click.option("--print-failures/--no-print-failures", default=False)
@click.option("--all/--no-all", default=False)
def fuzz(file_path, function_name, print_failures, all):
    # type: (str, str, bool, bool) -> None
    """
    TODO
    Args:
        file_path:
        function_name:
        print_failures:
        all:

    Returns:

    """
    if all:
        pass  # TODO after stub file gen is in
    else:  # TODO
        result_json = list()
        result_json.append(run_fuzzer(file_path, function_name))
        # print(result_json)
        default_print(result_json, print_failures=print_failures)


def flat_func_app(func, args):
    # type: (Callable[..., B], List[A]) -> B
    """Applys a function to a list of arguments

    Args:
        func: A function which we want to apply
        args: The list of arguments

    Returns:
        The output of calling func on args
    """
    return func(*args)


def class_func_app(class_instance,  # type: CLS
                   func,  # type: Callable[..., B]
                   func_args  # type: List[A]
                   ):
    # type: (...) -> B
    """

    Args:
        class_instance: An instance of a class
        func: The class function we want to evaluate
        func_args: The arguments to the function

    Returns:
        The class function func applied to the arguments func_args
    """
    # call the function with the instance
    return func(*([class_instance] + func_args))


def get_function(file_name, function_name):
    # type: (str, str) -> Callable[..., Any]
    """Gets the callable function with name function_name

    Args:
        file_name: The file where our function is defined
        function_name: The name of the function we'd like to load
            programatically

    Returns:
        The callable function.
    """
    funcs = function_name.split(".")
    if len(funcs) == 1:
        return getattr(__import__(file_name), funcs[0])
    else:
        return getattr(getattr(__import__(file_name), funcs[0]), funcs[1])


def fuzz_example(file_name,  # type: str
                 function_name,  # type: str
                 class_instance=None,  # type: Optional[Any]
                 ):
    # type: (...) -> Dict[Any, Any]
    """Type fuzzes a single example

    Args:
        file_name: The file name where the function we'd like to fuzz is located
        function_name: The name of the function we'd like to fuzz
        class_instance: The instance of the class this function is a member of
            if any.

    Returns:
        A JSON object describing which combinations of type instances were
        successful.
    """
    # Import the method we are interested in
    func = get_function(file_name, function_name)

    # Examine the imported function for annotations and parameters
    func_params = signature(func).parameters

    # Get the names of the parameters
    param_names = list(func_params.keys())

    # Get the total number of parameters
    total_num_params = len(signature(func).parameters)

    # Get the names of the parameters with default arguments
    default_param_names = [k for k, v in func_params.items()
                           if v.default is not Parameter.empty]

    num_params = total_num_params - len(default_param_names)

    # If we are using a class instance then the number of parameters needs to
    # be decremented by 1 to account for the self argument
    if class_instance:
        num_params -= 1

    # annotations = func.__annotations__

    instances = get_instances()

    # instances = get_dummy()
    all_inputs = list(product(*repeat(instances, num_params)))

    result_dict = {"function_to_type": function_name,
                   "arg_names": param_names,
                   "results": {"successes": defaultdict(list),
                               "failures": defaultdict(list)
                               }
                   }

    for input_args in all_inputs:

        types_only = [x[0] for x in input_args]
        args_only = [x[1] for x in input_args]

        try:
            if class_instance is None:
                flat_func_app(func, args_only)
                result_dict['results']['successes'][str(types_only)[1:-1]].append(args_only)
            else:
                class_func_app(class_instance, func, args_only)
                result_dict['results']['successes'][str(types_only)[1:-1]].append(args_only)

        except Exception as e:
            result_dict['results']['failures'][str(types_only)[1:-1]].append(args_only)

    return result_dict


def run_fuzzer(file_path, function_name):
    # type: (str, str) -> Dict[Any, Any]
    path = os.path.split(file_path)
    file_name = path[-1][:-3]
    path_str = os.path.join(*path[:-1])
    sys.path.append(path_str)

    # Check function name to see if it is nested in a class
    funcs = function_name.split(".")

    # NOTE: The maximum class depth is 2.
    if len(funcs) == 2:
        # Step 1, fuzz the constructor
        # Get the name of the class
        constructor_name = funcs[0]

        # Fuzz the class constructor so we can instantiate it
        valid_constructor_calls_json = fuzz_example(file_name, constructor_name)

        # Get valid constructor types and args
        good_constr_args = list(valid_constructor_calls_json["results"]["successes"].values())

        # TODO: run over all (?) successful class instances

        # Instantiate the class
        class_constr = get_function(file_name, constructor_name)
        class_instance = class_constr(*(good_constr_args[0][0]))

        # Fuzz the function using single instance of the class
        return fuzz_example(file_name, function_name, class_instance)

    elif len(funcs) == 1:
        return fuzz_example(file_name, function_name)
    else:
        raise ValueError("{} must either be the name of a function or a [single nested] class "
                         "method".format(function_name))


if __name__ == "__main__":
    main()
