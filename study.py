import pprint
import os
from collections import defaultdict
from command_helper import run_command, find_bugfixes, linux_info, test_info, find_commits_with_fix_tags
import dateparser
import datetime

#MIN_DATE = "October 1 2016"
MIN_DATE = "November 1 2016"
MAX_DATE = "November 15 2016"

def get_recent_non_merge_commits():
    args = ["git log  --pretty=oneline --no-color --since='{0}' --no-merges".format(MIN_DATE)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]

    commit_objs = []
    for h in hashes:
        stdout = run_command("git show --quiet {0} --format='%ad'".format(h))

        lines = stdout.decode("utf-8").split("\n")
        assert len(lines) == 2
        assert len(lines[1]) == 0
        date = lines[0].strip()
        commit_obj = {'hash': h, 'date': dateparser.parse(date)}
        commit_objs.append(commit_obj)

    return commit_objs

def find_lines_changed(commit):
    args = "git diff {0}~1 {0} --unified=0 --no-color".format(commit)
    output = run_command(args)
    lines = output.decode("utf-8").split("\n")
    DELIM = "@@"

    plus_filename = None
    line_ranges = []
    results = {}
    for l in lines:
        if l.startswith("+++ ") or l.startswith("--- "):
            if l.startswith("+++ ") and plus_filename is not None:
                results[plus_filename] = line_ranges
                line_ranges = []

            filename = l[len("+++ "):]
            if filename.startswith("a/") or filename.startswith("b/"):
                filename = filename[len("a/"):]

            # Can't use the --- filename since if we add/remove a file it could be /dev/null
            if l.startswith("+++ "):
                plus_filename = filename

        elif l.startswith(DELIM):
            plus = l.find("+")
            end_delim = l.find(DELIM, len(DELIM))

            lines_added = l[plus+len("+"):end_delim].strip()

            # We only care about lines added (something like 315 or 315,5)
            split = lines_added.split(",")
            assert len(split) <= 2 and len(split) > 0
            line_num = int(split[0])
            length = 1
            if len(split) == 2:
                length = int(split[1])

            if length > 0:
                # Want to store ranges as [start, end] inclusive on both sides
                end_line = line_num + length - 1
                line_ranges.append((line_num, end_line))

    results[plus_filename] = line_ranges
    return results


def get_line_history(commit, filename, start_line, end_line, min_date, max_date):
    print("Finding changes for L{1},{2}:{0}".format(filename, start_line, end_line))
    args = "git log -L{0},{1}:{2} --since='{3}' --before='{4}' --no-merges --no-color --pretty=oneline {5}".format(
        start_line, end_line,
        filename,
        min_date, max_date,
        commit)
    output = run_command(args)
    lines = output.decode("utf-8").split("\n")

    commits = []
    bad_start_symbols = ["+", "-", "diff", "@@"]
    for l in lines:
        if len(l) == 0 or any(l.startswith(b) for b in bad_start_symbols):
            continue

        # The line should look something like:
        # a8348bca2944d397a528772f5c0ccb47a8b58af4 crypto: algif_hash - Fix whatever...
        # We want the hash
        commit = l[:l.find(" ")]
        commits.append(commit)
    return commits

def main():
    info = linux_info
    os.chdir(info["path"])

    bug_fix_hashes = set(find_commits_with_fix_tags(MIN_DATE))

    recent_commits = get_recent_non_merge_commits()

    # Ignore first commit
    recent_commits = recent_commits[:-1]
    overlaps = defaultdict(list)
    for c in recent_commits:
        h = c['hash']
        # Find other changes to this line a week before
        min_date = c['date'] - datetime.timedelta(days=7)
        # Ignore changes to this line on the same day (in case the bug was immediately fixed
        # or there were just a bunch of commits at once)
        max_date = c['date'] - datetime.timedelta(days=1)
        print("Looking at commit {0}".format(h))
        changes = find_lines_changed(h)
        print("Changes are {0}".format(changes))
        for fname, line_changes in changes.items():
            for (start_line, end_line) in line_changes:
                commits_list = get_line_history(h, fname, start_line, end_line,
                                                min_date, max_date)
                commits = set(commits_list)

                hash_overlaps = bug_fix_hashes & commits
                for buggy_commit_hash in hash_overlaps:
                    overlap_obj = {'fname': fname,
                                   'start_line': start_line, 'end_line': end_line,
                                   'fix_commit': c}
                    print(buggy_commit_hash)
                    overlaps[buggy_commit_hash].append(overlap_obj)

                if len(hash_overlaps) > 0:
                    continue

    pprint.pprint(overlaps)

if __name__ == "__main__":
    main()
