"""
GrIFT is fuzzy typing is a python type fuzzer which can be used to type check
python modules, files, and single functions.
"""


import os
import sys
import json
from collections import defaultdict
from inspect import signature

from instances import *
from itertools import product, repeat

import click


# Set the environment codec variables so that click is callable from python3
if 'linux' in sys.platform:
    os.environ['LC_AL'] = "C.UTF-8"
    os.environ['LANG'] = "C.UTF-8"
else:
    os.environ['LC_AL'] = "en_US.utf-8"
    os.environ['LANG'] = "en_US.utf-8"


@click.group()
def main():
    pass


    """
JSON SPEC

    [
        {
        function_to_type : addOnes
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


def print_thin_bar(width):
    print("─" * width)


def print_thick_bar(width):
    print("━" * width)


def default_print(json_obj):
    for func in json_obj:
        indent = 30
        width = 70
        print_thick_bar(width)

        print(" "*(indent-2) + "TESTED\n" + str(func["function_to_type"]))
        results = func["results"]

        print("\n" + " "*(indent-3) + "SUCCESSES")

        print("─"*indent + "┬" + "─"*(width-indent-1))
        print(" "*((indent//2)-2) + "type" + " "*((indent//2)-2) + "│" + "   " + "instance")
        print("─"*indent + "┼" + "─" * (width - indent - 1))

        for types, insts in results["successes"].items():
            print(types.rjust(indent-1) + " │ ", insts[0])

        print("\n\n" + " "*(indent-3) + "FAILURES")

        print("─"*indent + "┬" + "─"*(width-indent-1))
        print(" "*((indent//2)-2) + "type" + " "*((indent//2)-2) + "│" + "   " + "instance")
        print("─"*indent + "┼" + "─" * (width - indent - 1))

        for types, insts in results["failures"].items():
            print(types.rjust(indent-1) + " │ ", insts[0])
        print_thick_bar(width)


def show_results(typeAccum):
    for (typeAnnotation, inst) in typeAccum:
        print(typeAnnotation+ "│", inst)


@main.command("fuzz")
@click.argument("file-path")
@click.argument("function-name")
def fuzz(file_path: str, function_name: str):
    result_json = list()
    result_json.append(run_fuzzer(file_path, function_name))
    default_print(result_json)


def run_fuzzer(file_path: str, function_name: str):
    path = os.path.split(file_path)
    file_name = path[-1][:-3]
    path_str = os.path.join(*path[:-1])

    # Import the method we are interested in
    sys.path.append(path_str)
    func = getattr(__import__(file_name), function_name)

    # Examine the imported function for annotations and parameters
    num_params = len(signature(func).parameters)
    annotations = func.__annotations__

    instances = get_instances()
    all_inputs = list(product(*repeat(instances, num_params)))


    result_dict = {"function_to_type": function_name,
                   "results": {"successes": defaultdict(list),
                               "failures": defaultdict(list)
                               }
                   }

    for input_args in all_inputs:
        types_only = [x[0] for x in input_args]
        args_only = [x[1] for x in input_args]

        try:
            func(*args_only)
            result_dict['results']['successes'][str(types_only)[1:-1]].append(args_only)

        except:
            result_dict['results']['failures'][str(types_only)[1:-1]].append(args_only)

    return result_dict # todo make work over


if __name__ == "__main__":
    main()