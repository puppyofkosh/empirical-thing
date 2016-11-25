# Look for commits with "Fixes: " in the log
import os
import re
from collections import defaultdict

from command_helper import run_command, find_bugfixes, linux_info


#MIN_DATE = "November 15 2016"
MIN_DATE = "January 1 2013"

def find_commits_with_fix_tags():
    args = ["git log --grep 'Fixes: ' --since='{0}' --no-color --no-merges".format(MIN_DATE)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")
    p = re.compile(r'Fixes:\s+(\w+)')
    commit_regex = re.compile(r'^commit (\w+)$')

    fix_map = defaultdict(set)
    current_commit = None
    for l in lines:
        res = commit_regex.search(l)
        if res is not None:
            # Line is telling us which commit we're looking at
            current_commit = res.group(1)
            continue

        # Check if the line tell us which commit the current commit fixes
        res = p.search(l)
        if res is not None:
            buggy_commit = res.group(1)
            fix_map[current_commit].add(buggy_commit)

    return fix_map

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

    fix_map = find_commits_with_fix_tags()
    buggy_fixes = find_broken_fixes(fix_map)

    print(buggy_fixes)
    
    prop = len(buggy_fixes) * 1.0 / len(fix_map)
    print("Number of fixes: {0}".format(len(fix_map)))
    print("Number of buggy fixes: {0}".format(len(buggy_fixes)))
    print("Proportion of fixes which themselves had to be fixed: {0}".format(prop))
    
if __name__ == "__main__":
    main()
