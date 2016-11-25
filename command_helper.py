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
# Return hashes for commits with the word bug in them in most recent -> least recent order
def find_bugfixes(min_date):
    args = ["git log --grep 'bug' --since='{0}' --pretty=oneline --no-color --no-merges".format(min_date)]
    stdout = run_command(args)
    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]
    return hashes
