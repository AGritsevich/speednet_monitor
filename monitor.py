#!/usr/bin/python3

import speedtest
import datetime
import time
import subprocess

file_name = "monitor.data"
st = speedtest.Speedtest()
Mbps = 1000*1000

while 1:
    try:
        f = open(file_name, "a")
        now = datetime.datetime.now()
        date = "{0:>19}".format(now.strftime("%Y-%m-%d %H:%M:%S"))
        download = "{0:>3.3f} Mbps".format(st.download() / Mbps )
        upload = "{0:>3.3f} Mbps".format(st.upload() / Mbps)
        ping = "{0:>2} ms".format(st.results.ping)

        f.writelines(f"{date}. d/u/p = {download} / {upload} / {ping} : {st.results.server['host']}\n")
        print(f"{date}. d/u/p = {download} / {upload} / {ping} : {st.results.server['host']}\n")

        f.close()
    except:
        print =("Test period have some fail. Doesn't care. Go on.")

    # git ones per day
    print("commiting")
    timeout = 10 # sec
    command_commit=["git", "commit", file_name, "-m", date]
    command_push=["git", "push", "origin", "HEAD"]
    commit = subprocess.Popen(command_commit, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    push = subprocess.Popen(command_push, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        out = commit.communicate(timeout = timeout)
        print(f"Commit out:")
        print(out)
        
        out = push.communicate(timeout = timeout)
        print(f"Push out:")
        print(out)
        #if proc.returncode == 0:
            #print()
    except subprocess.TimeoutExpired:
        commit.kill()
        push.kill()
    except :
        print =("Commit period have some fail. Doesn't care. Go on.")

    print("sleep for 1h")
    time.sleep(3600)
