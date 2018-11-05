##################################################
# AUTHOR : Xin XUE
# CREATED_AT : 2016-07-28
# LAST_MODIFIED : 2016-07-28 
# Position : .sh
# Purpose : stop two programs
# Excute Command: bash stop.sh
##################################################
#!/bin/bash
pgrep -fl ".*python.*cpu_load"|cut -d ' ' -f 1|xargs kill -9
