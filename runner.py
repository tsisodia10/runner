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

#add rules ---- check if count is valid
def check_count():
  if (args.count>1):
      print("Count -",sys.argv)

      # --- execute ping command with -c 
      exitCode = os.system(f'ping -c {args.count} google.com')
      if exitCode == 0:
          print("Success")
          # --- Success tracing
          success_tracing()
      else: 
          error_tracing()
         
if args.mode == 'debug':
      print("DEBUGGING MODE")
      debug=os.system(f'ping -c {args.count} -d google.com')
      print(debug)
else:
      print("MANUAL")
      help=os.system(f'ping -h')     
      print(help) 


def success_tracing():
      print("Tracing Successful execution --------------------------------------------------------\n")
      pingParsing = os.system(f'pingparsing google.com -c {args.count}')
      debug = os.system(f'ping -c {args.count} -d google.com ')
      print(pingParsing)
      print(debug)
      
def error_tracing():
      # --- while failed count is less than 2, it will execute till condition become false
      while args.failed < 2:
            exitCode = os.system(f'ping -c {args.count} google.com')
            args.failed = args.failed+1
          
      print("ExitCode ----- \n",exitCode)
          
      print("Tracing memory usage of failed execution -----------------------------------------------------------\n")
      sysTrace = os.system(f'strace ping -c {args.count} google.com')
      print("Tracing Failed execution -----------------------------------------------------------\n")
      pingParsing = os.system(f'pingparsing google.com -c {args.count}')
      print(sysTrace)
      print(pingParsing)


def main():
        check_count()
        # uname_func()
        #disk_func()
       
main()