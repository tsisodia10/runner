
import argparse
import os
import subprocess
import sys
import threading
import time
import shlex

parser = argparse.ArgumentParser(description='Manage rules')

parser.add_argument('-com', '--command',
                     action='store', 
                     required=True, dest='command')

parser.add_argument('-c', '--count', type=int,
                     action='store', 
                     required=True, dest='count')

# parser.add_argument('-fc', '--failed-count', type=int,
#                      action='store', 
#                      required=True, dest='failed')

parser.add_argument('-m', '--mode', 
                     action='store', choices={'debug','help'}, dest='mode')


args = parser.parse_args()


class TestThreading(object):

 # --- check count and also checks the returncode - if it's success or failure 
 def __init__(self, interval=1):

      self.interval = interval

      thread = threading.Thread(target=self.run, args=())
      thread.start()
      thread.join()


 def run(self, timeout=0):
        num = 0
          # --- check and execute ping command with -c   
        while num < args.count: 
          print("CALLING 1st process")
          process = subprocess.Popen(shlex.split(args.command), 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
          # output, errors = process.communicate()                           
          returncode = process.returncode 
          
          # print(output)
          # print(errors)  
          process.poll()
          proc = process.pid
          # str_proc = str(proc)
          print("Printing pid", proc) 
          num = num + 1                   
          time.sleep(0.2)
          if returncode == 0:                         
            print("Successful execution")
          else:
            def netTracing():
             command = str(args.command)
             print("Calling NETSTAT process")
             netTrace = subprocess.Popen(["ps", "-p", str(proc)], shell=True, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            #  print(netTrace.stdout)
            #  print(netTrace.stderr)
             output, errors = netTrace.communicate()
             print(output)
             print(errors)
             netTrace.poll()
             time.sleep(0.2)
            #  print(netTrace.stdout.readline())

            def sysTracing():
             print("Calling SYSTRACE process")  
             sysTrace = subprocess.Popen(["sudo","strace", "-p", str(proc)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

             output, errors = sysTrace.communicate()
             sysTrace.poll()  
            #  print(sysTrace.stdout)
            #  print(sysTrace.stderr)   
             print(output)
             print(errors) 
             time.sleep(0.2)             
             print("SYSTRACE RUN FINISHED")   

            a = threading.Thread(target=netTracing, name='Thread-a')
            print("NOW RUNNING NETSTAT")
            a.start()
            a.join()
            b = threading.Thread(target=sysTracing, name='Thread-b')
            print("NOW RUNNING SYSTRACE")
            b.start()
            b.join()
          
          
                  
tr = TestThreading()
