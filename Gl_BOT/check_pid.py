import psutil
pid = 30053
if psutil.pid_exists(pid):
    print("a process with pid %d exists" % pid)
else:
    print("a process with pid %d does not exist" % pid)
