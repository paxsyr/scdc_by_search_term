import argparse
import json
import sys


def print_job_title_and_company(
    job_page,
):
    employer_start_index = job_page.index("Employer:") + 18
    employer_end_index = job_page.index(")\n<br>\n<") - 6
    print(co_op_name, "-", job_page[employer_start_index:employer_end_index])


parser = argparse.ArgumentParser(
    description="Search a .json, containing contents of SCDC job postings, for search terms"
)
parser.add_argument("file_name", help="the name of the file to search")
parser.add_argument(
    "search_terms", nargs="+", help="the terms to search the jobs postings for"
)
parser.add_argument(
    "-a",
    "--and_search",
    action="store_true",
    help="only give results that have all the search terms, rather than those with at least one",
)
parser.add_argument(
    "-i",
    "--case_insensitive",
    action="store_true",
    help="whether or not all the search terms are all case insensitive",
)
args = parser.parse_args()

if args.and_search:
    search_type = "AND"  # must be "AND" or "OR"
else:
    search_type = "OR"

if search_type != "AND" and search_type != "OR":
    print(
        "ERROR: Please choose to search for either the AND or the OR of the search terms"
    )
    sys.exit()

with open(args.file_name, "r") as fp:
    scdc_dump = json.load(fp)

job_count = 0

for co_op_name in scdc_dump.keys():
    if search_type == "AND":
        skip_job = False

        for term in args.search_terms:
            if (
                args.case_insensitive
                and term.casefold() not in scdc_dump[co_op_name].casefold()
            ) or (not args.case_insensitive and term not in scdc_dump[co_op_name]):
                skip_job = True

        if not skip_job:
            job_count += 1
            print_job_title_and_company(scdc_dump[co_op_name])

    elif search_type == "OR":
        for term in args.search_terms:
            if (
                args.case_insensitive
                and term.casefold() in scdc_dump[co_op_name].casefold()
            ) or (not args.case_insensitive and term in scdc_dump[co_op_name]):
                job_count += 1
                print_job_title_and_company(scdc_dump[co_op_name])
                break

    else:
        print(
            "ERROR: Please choose to search for either the AND or the OR of the search terms"
        )
        sys.exit()

print()

if len(args.search_terms) == 1:
    print(f"The search for '{args.search_terms[0]}' resulted in", job_count, "matches")
else:
    print(
        "The search for the",
        search_type,
        "of the search terms",
        args.search_terms,
        "resulted in",
        job_count,
        "matches",
    )
