#!/usr/bin/env python3

#
#          FILE:  runner.py
#
#
#   DESCRIPTION:  Manage rules
#
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#        AUTHOR:  Twinkll Sisodia
#       COMPANY:  Red Hat
#       VERSION:  1.0
#       CREATED:  08/21/2020
# ===============================================================================

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

parser.add_argument('-m', '--mode', 
                     action='store', choices={'debug','help'}, dest='mode')

parser.add_argument('--sys-trace', '--sys', 
                     action='store', choices={'network','memory'}, dest='sys')

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
          output, errors = process.communicate()                           
          print(shlex.split(args.command))
          print(output)
          print(errors)  
          process.poll()
          proc = process.pid
          # str_proc = str(proc)
          print("Printing pid", proc) 
          num = num + 1                   
          time.sleep(0.2)

          if process.returncode == 0:                         
            print("Successful execution")
          else:
            def netTracing():
             command = str(args.command)
             print("Calling NETSTAT process")
             netTrace = subprocess.Popen(["netstat", "-at", " | ", "grep", str(proc)],  
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
             sysTrace = subprocess.Popen(["sudo","strace","-s", "80", "-fp", str(proc)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

             sysCommand = shlex.split(args.sys)
             sysTrace1 = subprocess.Popen(["sudo","strace","-e", "trace=","sysCommand", "-p", str(proc)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
             output1, errors1 = sysTrace1.communicate()                   
             output, errors = sysTrace.communicate()
             sysTrace.poll()  

             print(output1)
             print(errors1) 
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
