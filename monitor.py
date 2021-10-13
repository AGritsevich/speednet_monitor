#!/usr/bin/python3

import speedtest
import datetime
import time
import subprocess

file_name = "monitor.data"
st = speedtest.Speedtest()

while 1:
    f = open(file_name, "a")
    now = datetime.datetime.now()
    date = "{0:>19}".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    download = "{0:>18}".format(st.download())
    upload = "{0:>18}".format(st.upload())
    ping = "{0:>6}".format(st.results.ping)

    f.writelines("%s. d/u/p = %s / %s / %s : %s\n" % (date, download, upload, ping, st.results.server['host']))
    print("%s. d/u/p = %s / %s / %s : %s \n" % (date, download, upload, ping, st.results.server['host']))

    f.close()

    # git ones per day
    print("commiting")
    timeout = 10 # sec
    command_commit=["git", "commit", file_name, "-m", date]
    command_push=["git", "push", "origin", "HEAD"]
    proc1 = subprocess.Popen(command_commit, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc2 = subprocess.Popen(command_push, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        out, err = proc1.communicate(timeout = timeout)
        print(out)
        print(err)
        out, err = proc2.communicate(timeout = timeout)
        print(out)
        print(err)
        #if proc.returncode == 0:
            #print()
    except subprocess.TimeoutExpired:
        proc1.kill()

    print("sleep for 1h")
    time.sleep(3600)
