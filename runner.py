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


# --- add rules 
def check_count():
      num = 0
      # --- check and execute ping command with -c 
      while num < args.count:
        
          process = subprocess.run('ping -c 2 google.com', shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)      
          print('Returncode: ', process.returncode)  
          print('Have {} bytes in stdout:\n{}'.format(
                len(process.stdout),
                process.stdout.decode('utf-8'))
          )    
          print('Have {} bytes in stderr: {!r}'.format(
                len(process.stderr),
                process.stderr.decode('utf-8'))
          )              

        
          num = num + 1
          if process.returncode == 0:
             print("Success")
             # --- Success tracing
             success_tracing()
          else: 
             error_tracing()


# --- function which displays tracing for successful execution
def success_tracing():

      print("\n\nTRACING SUCCESSFUL EXECUTION -------------------------------------\n")

      # --- execute ping and parse the result
      pingParsing = os.system(f'pingparsing google.com -c {args.count}')
      print("\n\nMEMORY AND DISK USAGE --------------------------------------------\n")

      # --- memory usage output
      sysTrace = os.system(f'strace ping -c {args.count} google.com')

      print(sysTrace)
      print(pingParsing)

      # --- debug mode
      if args.mode == 'debug':
          print("DEBUGGING MODE")
          debug=os.system(f'ping -c {args.count} -d google.com')
          print(debug)

      # --- help mode
      if args.mode == 'help':
          print("MANUAL")
          help=os.system(f'ping -h')     
          print(help) 
      
      
# --- function whih displays tracing for failed execution      
def error_tracing():
      
      # --- numc - variable flag
      numc = 0
      
      # --- while failed count is less than 2, it will execute till condition become false
      while numc < args.failed:
            process = subprocess.run('ping -c 2 google.com', shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE) 
            numc = numc + 1   

      print("Returncode : \n",process.returncode)   
      print("TRACING MEMORY USAGE OF FAILED EXECUTION--------------------------------\n")
      sysTrace = os.system(f'strace ping -c {args.count} google.com')
      print("TRACING FAILED EXECUTION------------------------------------------------\n")
      pingParsing = os.system(f'pingparsing google.com -c {args.count}')
      netTrace = subprocess.run(['netstat','ping','-s','google.com'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
      print(sysTrace)
      print(pingParsing)
      print(netTrace)
      print("Use the debug mode to trace errors : usage : ping -d")
      
      # --- debug mode
      if args.mode == 'debug':
          print("DEBUGGING MODE")
          debug=os.system(f'ping -c {args.count} -d google.com')
          print(debug)

      # --- help mode
      if args.mode == 'help':
          print("MANUAL")
          help=os.system(f'ping -h')     
          print(help)


# --- main function
def main():
        check_count()
       
main()