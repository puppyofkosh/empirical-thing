import os
import subprocess

linux_info = {
#    "path": "/home/puppyofkosh/safer-c-compiler",
    "path": "/home/puppyofkosh/linux",
}

test_info = {
    "path": "test-repo"
}


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
def find_bugfixes():
    args = ["git log --grep 'bug' --since='January 1 2015' --pretty=oneline --no-color"]
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
    minus_filename = None
    line_ranges = []
    results = {}
    for l in lines:
        if l.startswith("+++ ") or l.startswith("--- "):
            if l.startswith("+++ ") and plus_filename is not None:
                print("Done for " + plus_filename)
                results[plus_filename] = line_ranges
                line_ranges = []

            filename = l[len("+++ "):]
            if filename.startswith("a/") or filename.startswith("b/"):
                filename = filename[len("a/"):]

            if l.startswith("--- "):
                minus_filename = filename
            elif l.startswith("+++ "):
                plus_filename = filename
                assert plus_filename == minus_filename

        elif l.startswith(DELIM):
            minus = l.find("-")
            plus = l.find("+")
            end_delim = l.find(DELIM, len(DELIM))

            lines_removed = l[minus+len("-"):plus].strip()
            lines_added = l[plus+len("+"):end_delim].strip()
            print(lines_removed)
            print(lines_added)

            # We only care about lines added (something like 315 or 315,5)
            split = lines_added.split(",")
            assert len(split) <= 2 and len(split) > 0
            line_num = int(split[0])
            length = 0
            if len(split) == 2:
                length = int(split[1])
            line_ranges.append((line_num, length))

    results[plus_filename] = line_ranges
    print(results)
if __name__ == "__main__":
    info = linux_info

    os.chdir(info["path"])
    find_lines_changed("HEAD")
    #find_bugfixes()
