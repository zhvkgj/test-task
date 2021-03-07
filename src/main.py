import sys
from collections import namedtuple

from radon.raw import analyze, Module
from radon.metrics import mi_visit, mi_rank
from radon.complexity import cc_visit, cc_rank
from radon.cli.tools import iter_filenames


def analyze_directory(name: str, exclude=None, ignore=None):
    """Iter through filenames starting from the `name` directory
    and collecting metrics info about each file into dictionary.
    Optional `exclude` filters can be passed as a comma-separated
    string of regexes, while `ignore` filters are a comma-separated list of
    directory names to ignore.
    """
    DirResult = namedtuple('Result', ['cc', 'mi', 'raw'])

    dict_with_dir_results = {}
    for filename in iter_filenames([name], exclude=exclude, ignore=ignore):
        with open(filename) as f_obj:
            source = f_obj.read()
        # get Cyclomatic Complexity blocks
        cyclomatic = extract_cyclomatic_complexity(cc_visit(source))
        # get Maintainability score
        mi = mi_rank(mi_visit(source, True))
        # get raw metrics
        raw = analyze(source)
        dict_with_dir_results[filename] = DirResult(cc=cyclomatic, mi=mi, raw=raw)
    return dict_with_dir_results


def extract_cyclomatic_complexity(blocks: list):
    """Extract cyclomatic complexity score from list of `Function` or `Class` namedtuples.
    Return list of dictionaries corresponding to each function, method or class.
    """
    list_of_cc = []
    for block in blocks:
        list_of_cc.append({'letter': block.letter, 'name': block.fullname,
                           'rank': cc_rank(block.complexity)})
    return list_of_cc


def print_enumerated_result(dir_results: dict):
    """Prints formatted string consist of methods' and
    classes' cyclomatic complexity, maintainability rank and
    from `dir_results`.
    """
    def format_cc_info(cc_info: list):
        result = []
        for cur_decl in cc_info:
            result.append(f"\t{cur_decl['letter']} {cur_decl['name']} "
                          f"complexity rank: {cur_decl['rank']}\n")
        return "".join(result)

    def format_mi_info(mi_info: int):
        return f"\tMaintainability rank: {mi_info}"

    def format_raw_info(raw_info: Module):
        return f"\tloc: {raw_info.loc}\n" \
               f"\tlloc: {raw_info.lloc}\n" \
               f"\tsloc: {raw_info.sloc}\n"

    list_of_str_with_res = []
    for num, (filename, dir_res) in enumerate(dir_results.items()):
        list_of_str_with_res.append(f"  {num + 1}. {filename}:\n"
                                    f"{format_cc_info(dir_res.cc)}\n"
                                    f"{format_mi_info(dir_res.mi)}\n"
                                    f"{format_raw_info(dir_res.raw)}")
    for res in list_of_str_with_res:
        print(res)


def harvest_and_print_the_metrics(name: str, exclude, ignore):
    """Iter through filenames starting from the `name` directory
    and printing metrics info about each file into dictionary.
    Optional `exclude` filters can be passed as a comma-separated
    string of regexes, while `ignore` filters are a comma-separated list of
    directory names to ignore.
    """
    metrics_res_under_dir = analyze_directory(name, exclude, ignore)
    print_enumerated_result(metrics_res_under_dir)


directory = sys.argv[1] if len(sys.argv) > 1 else '.'
exclude_files = sys.argv[2] if len(sys.argv) > 2 else None
ignore_files = sys.argv[3] if len(sys.argv) > 3 else None

harvest_and_print_the_metrics(directory, exclude_files, ignore_files)
