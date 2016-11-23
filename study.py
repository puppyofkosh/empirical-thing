import os
import subprocess

linux_info = {
#    "path": "/home/puppyofkosh/safer-c-compiler",
    "path": "/home/puppyofkosh/linux",
}


#TODO update regex to be [bug|fix]
def find_bugfixes():
    args = ["git log --grep 'bug' --since='January 1 2015' --pretty=oneline --no-color"]
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    stdout, stderr = proc.communicate()
    if len(stderr) > 0:
        print(stderr)
        raise RuntimeError("Wrote to stderr !?")

    lines = stdout.decode("utf-8").split("\n")

    hashes = [l.split(" ")[0] for l in lines if len(l) > 0]
    print(hashes)
    print(len(hashes))


# Traverse logs in reverse order

if __name__ == "__main__":
    info = linux_info

    os.chdir(info["path"])
    find_bugfixes()
