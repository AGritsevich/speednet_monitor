#!/usr/bin/python3

import speedtest
import datetime
import time
import subprocess

file_name = "monitor.data"
timeout = 10
st = speedtest.Speedtest()
#st.get_best_server(st.set_mini_server("http://speedtest.test.fr/"))
#st.get_best_server()

while 1:
    f = open(file_name, "a")
    now = datetime.datetime.now()
    data = "{0:_>20}".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    download = "{0:>20}".format(st.download())
    upload = "{0:>20}".format(st.upload())
    ping = "{0:>5}".format(st.results.ping)
    f.writelines("%s. d/u/p = %s / %s / %s : %s\n" % (data, download, upload, ping, st.get_best_server()))
    print("%s. d/u/p = %s / %s / %s : %s \n" % (data, download, upload, ping, st.get_best_server()))

    f.close()

    # git ones per day
    print("commiting\n")
    command_commit=["git", "commit", file_name, "-m", data]
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

    print("slepp for 1h")
    time.sleep(3600) # Sleep for 3 seconds
