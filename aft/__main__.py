import click

from aft import fuzzer


from typing import Any, Dict, List, Union


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


@click.group()
def main():
    pass


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
        result_json.append(fuzzer.run_fuzzer(file_path, function_name))
        # print(result_json)
        default_print(result_json, print_failures=print_failures)


if __name__ == '__main__':
    main()
