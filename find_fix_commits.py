# Look for commits with "Fixes: " in the log
import os
import re
from collections import defaultdict

from command_helper import run_command, linux_info, find_commits_with_fix_tags

#MIN_DATE = "November 15 2016"
MIN_DATE = "January 1 2015"


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

def main():
    info = linux_info
    os.chdir(info["path"])

    fix_map = find_commits_with_fix_tags(MIN_DATE)
    buggy_fixes = find_broken_fixes(fix_map)

    print(buggy_fixes)
    
    prop = len(buggy_fixes) * 1.0 / len(fix_map)
    print("Number of fixes: {0}".format(len(fix_map)))
    print("Number of buggy fixes: {0}".format(len(buggy_fixes)))
    print("Proportion of fixes which themselves had to be fixed: {0}".format(prop))
    
if __name__ == "__main__":
    main()
