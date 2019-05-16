import argparse
from typing import Any, Dict, List, Union

from aft import fuzzer


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


def console_entry():
    parser = argparse.ArgumentParser(prog="aft")
    parser.add_argument("file_path",
                        metavar="FILE",
                        help="Path to the file to fuzz")
    parser.add_argument("function_name",
                        metavar="FUNCTION_NAME",
                        help="Name of the function to fuzz")
    parser.add_argument("--print-failures",
                        default=False,
                        action="store_true",
                        help="Print failed inputs as well")
    parser.add_argument("--all",
                        default=False,
                        action="store_true",
                        help="Fuzz everything in the file")
    args = parser.parse_args()

    result_json = list()
    result_json.append(fuzzer.run_fuzzer(args.file_path, args.function_name))
    default_print(result_json, print_failures=args.print_failures)


if __name__ == '__main__':
    console_entry()
