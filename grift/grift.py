"""
GrIFT is fuzzy typing is a python type fuzzer which can be used to type check
python modules, files, and single functions.
"""


import os
import sys
import subprocess
import json
from collections import defaultdict

from instances import *

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
        indent = 10
        width = 40
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
    result_json = []
    result_json.append(run_fuzzer(file_path, function_name))
    default_print(result_json)


def run_fuzzer(file_path: str, function_name: str):
    path = os.path.split(file_path)
    file_name = path[-1][:-3]
    path_str = os.path.join(*path[:-1])

    instances = get_instances()
    result_dict = {"function_to_type": function_name, "results": {"successes": defaultdict(list), "failures": defaultdict(list)}}

    for (type_annotation, inst) in instances:
        # Write a file to be tested
        import_str = f"""import sys\nsys.path.append("{path_str}")\nfrom {file_name} import *\n"""
        call_str = f"{function_name}({str(inst)})"
        run_str = import_str + call_str

        # Write file to fuzz
        with open("current_test.py", "w") as f:
            f.write(run_str)

        try:
            with open("/dev/null", "w") as err:
                subprocess.run("python3 current_test.py",
                               shell=True,
                               check=True,
                               stderr=err)

            result_dict['results']['successes'][type_annotation].append(inst)

        except subprocess.CalledProcessError as grepexc:
            result_dict['results']['failures'][type_annotation].append(inst)

    return result_dict #todo make work over


if __name__ == "__main__":
    main()