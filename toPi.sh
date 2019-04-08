#!/bin/bash

piAddr='daniel@192.168.178.51'

scp ~/bin/pyScripts/uhr.py "$piAddr:~/bin/pyScripts/uhr.py"
ssh -t "$piAddr" 'sudo python3 ~/bin/pyScripts/uhr.py'
