import pprint
import os
from collections import defaultdict
import command_helper
from command_helper import run_command, try_run_command, find_bugfixes, linux_info, test_info, find_commits_with_fix_tags
import dateparser
import datetime

# line radius 10, 2 weeks, november 1 = 9 bugs

#MIN_DATE = "September 1 2016"
MIN_DATE = "October 1 2016"
MIN_DATE_DT = dateparser.parse(MIN_DATE)

MAX_DATE = "January 1 2017"
MAX_DATE_DT = dateparser.parse(MAX_DATE)

LINE_RADIUS = 20

def get_recent_non_merge_commits():
    args = ["git log --pretty=oneline --no-color --since='{0}' --no-merges".format(MIN_DATE)]
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
    args = "git show {0} --unified=0 --no-color --pretty=oneline --format=''".format(commit)
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


def get_line_history(commit, filename, start_line, end_line, radius, min_date, max_date):
    args = "git log -L{0},{1}:{2} --since='{3}' --pretty=oneline --format='commit:%H|%ad' {4}".format(
        max(start_line - radius, 1), end_line + radius,
        filename,
        MIN_DATE,
        commit)
    output, stderr = try_run_command(args)
    if len(stderr) > 0 and 'has only' in stderr.decode("utf-8") and radius > 0:
        return get_line_history(commit, filename, start_line, end_line, 0, min_date, max_date)
    elif len(stderr) > 0:
        raise RuntimeError(stderr)

    lines = output.decode("utf-8").split("\n")

    commits = {}
    for l in lines:
        if len(l) == 0 or not l.startswith("commit:"):
            continue

        # The line should look something like:
        # a8348bca2944d397a528772f5c0ccb47a8b58af4 crypto: algif_hash - Fix whatever...
        # We want the hash
        commit = l[l.find(":")+1:l.find("|")]
        date = dateparser.parse(l[l.find("|")+1:])
        if date >= min_date and date <= max_date:
            commits[commit] = date

    return commits

def main():
    info = linux_info
    os.chdir(info["path"])

    bug_fix_commits = command_helper.find_commits_with_fix_words(MIN_DATE_DT, MAX_DATE_DT)
    bug_fix_hashes = {c['hash'] for c in bug_fix_commits}
    #bug_fix_hashes = set(find_commits_with_fix_tags(MIN_DATE))

    print("Found {0} bug fixes".format(len(bug_fix_hashes)))

    # Ignore first commit
    bug_fix_commits = bug_fix_commits[:-1]
    overlaps = defaultdict(list)
    for c in bug_fix_commits:
        h = c['hash']
        # Find other changes to this line a week before
        min_date = c['date'] - datetime.timedelta(days=14)
        # Ignore changes to this line on the same day (in case the bug was immediately fixed
        # or there were just a bunch of commits at once)
        max_date = c['date'] - datetime.timedelta(days=1)
        print("Looking at commit {0}".format(h))
        changes = find_lines_changed(h)
        for fname, line_changes in changes.items():
            for (start_line, end_line) in line_changes:
                print("Getting line history")
                commit_dict = get_line_history(h, fname, start_line, end_line, LINE_RADIUS,
                                               min_date, max_date)
                commit_hashes = set(commit_dict.keys())

                hash_overlaps = bug_fix_hashes & commit_hashes
                for buggy_commit_hash in hash_overlaps:
                    overlap_obj = {'path': '{0},{1}:{2}'.format(start_line, end_line, fname),
                                   'fix_commit': c}
                    key = (buggy_commit_hash, commit_dict[buggy_commit_hash])
                    overlaps[key].append(overlap_obj)

                if len(hash_overlaps) > 0:
                    continue

    pprint.pprint(overlaps)
    print("Total number of fixes since {0}:{1}".format(MIN_DATE, len(bug_fix_hashes)))
    print("Number of buggy fixes found: {0}".format(len(overlaps)))

if __name__ == "__main__":
    main()
