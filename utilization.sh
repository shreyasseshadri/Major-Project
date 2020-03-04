#!/bin/bash

vm_id="$(whoami)"
file_name="util${vm_id}.txt"
if [ -f $file_name ] ; then
    echo "Removing previous utilization output"
    rm $file_name
fi
top -b -n3  | grep -f patterns.txt > $file_name
echo "CPU charecteristics taken"
timeout 3s bwm-ng -o csv > nw.txt
grep -f patterns.txt nw.txt >> $file_name
echo "Network charecteristics taken"
rm nw.txt
echo "id:${vm_id}" >> $file_name