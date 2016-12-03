import re
from collections import defaultdict
import subprocess
import dateparser

linux_info = {
#    "path": "/home/puppyofkosh/safer-c-compiler",
    "path": "/home/puppyofkosh/linux",
}

test_info = {
    "path": "test-repo"
}


def try_run_command(args):
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    stdout, stderr = proc.communicate()
    return stdout, stderr

def run_command(args):
    stdout, stderr = try_run_command(args)
    if len(stderr) > 0:
        print(stderr)
        raise RuntimeError("Wrote to stderr !?")
    return stdout

#TODO update regex to be [bug|fix]
# Return hashes for commits with the word bug in them in most recent -> least recent order
def find_bugfixes(min_date):
    args = ["git log --grep 'bug' --since='{0}' --pretty=oneline --no-color --no-merges".format(min_date)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]
    return hashes

def find_commits_with_fix_tags(min_date, max_date=None):
    argstr = "git log --grep 'Fixes: ' --since='{0}' --no-color --no-merges".format(min_date)
    if max_date is not None:
        argstr += " --before='{0}'".format(max_date)
    args = [argstr]
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

def find_commits_with_fix_words(min_date):
    args = [r"git log --grep='Reported-and-tested\|Fixes:\|Fix\|fix\|bug\|Acked-by' --pretty=oneline --format='commit:%H|%ad' --since='{0}' --no-merges".format(min_date)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    commits = []
    for tl in lines:
        l = tl.strip()
        if len(l) == 0:
            continue
        commit = l[l.find(":")+1:l.find("|")]
        date = dateparser.parse(l[l.find("|")+1:])
        if date >= min_date:
            ob = {'hash': commit, 'date': date}
            commits.append(ob)

    return commits

def get_commit_date(commit):
    args = ["git show {0} --pretty=oneline --format='%ad'".format(commit)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")
    return dateparser.parse(lines[0])
