import os
import subprocess

linux_info = {
#    "path": "/home/puppyofkosh/safer-c-compiler",
    "path": "/home/puppyofkosh/linux",
}

test_info = {
    "path": "test-repo"
}

MIN_DATE = "October 1 2016"

def run_command(args):
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    stdout, stderr = proc.communicate()
    if len(stderr) > 0:
        print(stderr)
        raise RuntimeError("Wrote to stderr !?")
    return stdout


#TODO update regex to be [bug|fix]
# Return hashes for commits with the word bug in them in most recent -> least recent order
def find_bugfixes():
    args = ["git log --grep 'bug' --since='{0}' --pretty=oneline --no-color --no-merges".format(MIN_DATE)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]
    return hashes

def get_recent_non_merge_commits():
    args = ["git log  --pretty=oneline --no-color --since='{0}' --no-merges".format(MIN_DATE)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]
    return hashes

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


def get_line_history(commit, filename, start_line, end_line):
    print("Finding changes for L{1},{2}:{0}".format(filename, start_line, end_line))
    args = "git log -L{0},{1}:{2} --since='{3}' --no-merges --no-color --pretty=oneline {4}".format(start_line, end_line,
                                                                                                    filename, MIN_DATE,
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
    #info = test_info
    info = linux_info
    os.chdir(info["path"])

    bug_fixes = set(find_bugfixes())

    recent_commits = get_recent_non_merge_commits()

    # TODO: undo
    #recent_commits = recent_commits[:25]

    # Ignore first commit
    recent_commits = recent_commits[:-1]
    overlaps = []
    for c in recent_commits:
        print("Looking at commit {0}".format(c))
        changes = find_lines_changed(c)
        print("Changes are {0}".format(changes))
        for fname, line_changes in changes.items():
            for (start_line, end_line) in line_changes:
                commits_list = get_line_history(c, fname, start_line, end_line)
                commits = set(commits_list)
                assert c in commits
                commits.remove(c)

                if len(bug_fixes & commits) > 0:
                    print("OVERLAP FOUND")
                    overlaps.append((c, fname, start_line, end_line, bug_fixes & commits))

    #find_lines_changed("HEAD")
    print("Overlaps are {0}".format(overlaps))
    

if __name__ == "__main__":
    main()
