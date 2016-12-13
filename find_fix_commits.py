# Look for commits with "Fixes: " in the log
import os
import re
from collections import defaultdict

import datetime
import calendar

import pprint
from command_helper import run_command, linux_info, find_commits_with_fix_tags,get_commit_date

#MIN_DATE = "November 15 2016"
#MIN_DATE = "January 1 2015"

MIN_DATE = "October 1 2016"
#MIN_DATE = "September 1 2016"

def find_broken_fixes(fix_map):
    # Fix map is of form {fix commit -> buggy commit}
    # We want to find fix commits which ARE buggy commits

    # commit -> commits which fixed it
    buggy_fixes = defaultdict(set)
    for fix_commit in fix_map:
        for other_fix_commit in fix_map:
            fc = {k for k in fix_map[other_fix_commit] if fix_commit.startswith(k)}
            if len(fc) > 0:
                buggy_fixes[fix_commit].add(other_fix_commit)

    return buggy_fixes

def count_buggy_fixes(buggy_fixes):
    # Map is of form: commit -> commits which fixed it
    # If commit X has 3 fixes: A, B, and C, then we have 3 buggy
    # fixes: X, A, and B
    count = sum(len(buggy_fixes[b]) for b in buggy_fixes)
    return count

def main():
    info = linux_info
    os.chdir(info["path"])

    fix_map = find_commits_with_fix_tags(MIN_DATE)
    buggy_fixes = find_broken_fixes(fix_map)

    print(buggy_fixes)

    prop = len(buggy_fixes) * 1.0 / len(fix_map)
    print("Number of fixes: {0}".format(len(fix_map)))
    print("Number of buggy fixes: {0}".format(len(buggy_fixes)))
    print("Number of buggy fixes if you count double-fixes: {0}".format(count_buggy_fixes(buggy_fixes)))
    print("Proportion of fixes which themselves had to be fixed: {0}".format(prop))


def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + int(month / 12))
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def count_by_month(commits):
    month_map = defaultdict(int)
    for fix in commits:
        date = get_commit_date(fix)
        key = datetime.date(date.year, date.month, 1)
        month_map[key] += 1
    return month_map

def get_buggy_fixes_by_month():
    info = linux_info
    os.chdir(info["path"])

    print("Finding commits with the tags")
    fix_map = find_commits_with_fix_tags(MIN_DATE)
    buggy_fixes = find_broken_fixes(fix_map)

    print("Getting buggy fixes...")
    month_to_num_buggy_fixes = count_by_month(buggy_fixes.keys())

    print("Getting total fixes...")
    month_to_total_fixes = count_by_month(fix_map.keys())

    final_map = {}
    for k,v in month_to_total_fixes.items():
        final_map[k] = {'total_fixes': v,
                        'buggy_fixes': month_to_num_buggy_fixes.get(k, 0)}

    return final_map

if __name__ == "__main__":
    #pprint.pprint(get_buggy_fixes_by_month())
    main()
