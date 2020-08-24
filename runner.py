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

parser.add_argument('-c', '--count', 
                     metavar='count', action='count', 
                     required=True, add_help=True, dest=count)

args = parser.parse_args()

#add rules ---- check if count is valid
if (args.count>1):
      print("Count -",sys.argv)

      # --- execute ping command with -c 
      exitCode = os.system(f'ping -c {args.count} google.com')
      if exitCode == 0:
          print("Success")