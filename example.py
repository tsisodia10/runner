import argparse
import os
import subprocess
import sys
import threading
import time

parser = argparse.ArgumentParser(description='Manage rules')

parser.add_argument('-c', '--count', type=int,
                     action='store', 
                     required=True, dest='count')

parser.add_argument('-fc', '--failed-count', type=int,
                     action='store', 
                     required=True, dest='failed')

parser.add_argument('-m', '--mode', 
                     action='store', choices={'debug','help'}, dest='mode')


args = parser.parse_args()


import time

import threading


class TestThreading(object):

 # --- check count and also checks the returncode - if it's success or failure 
 def __init__(self, interval=1):

      self.interval = interval

      thread = threading.Thread(target=self.run, args=())
      thread.start()


 def run(self):
      
        def check_count():
          print("CALLING 1st process")
          process = subprocess.Popen(["ping","-c 2", "google.com"], 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)  
            # output, errors = process.communicate()
          process.poll()
          proc = process.pid
          str_proc = str(proc)
          print("Printing pid", proc)
          self.stdout, self.stderr = process.communicate()
          print(self.stdout)
          print(self.stderr)
               
          def netTracing():
             print("Calling NETSTAT process")
             netTrace = subprocess.Popen(["netstat", "ping", "-at", "google.com"], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
             time.sleep(2)
             output, errors = netTrace.communicate()
             print(output)
             print(errors)
             netTrace.poll()

          def sysTracing():
             print("Calling SYSTRACE process")   
             sysTrace = subprocess.Popen(["strace", "-p", str_proc], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

             output, errors = sysTrace.communicate()
             sysTrace.poll()     
             print(output)
             print(errors)              
             time.sleep(2)
             print("SYSTRACE RUN FINISHED")   

       
          a = threading.Thread(target=netTracing, name='Thread-a')
          print("NOW RUNNING NETSTAT")
          a.start()
          a.join()
          b = threading.Thread(target=sysTracing, name='Thread-b')
          print("NOW RUNNING SYSTRACE")
          b.start()
          b.join()
          
        a1 = threading.Thread(target=check_count, name='Thread-a1')
        a1.start()
                        

tr = TestThreading()
