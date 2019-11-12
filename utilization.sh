top -b -n3  | grep -f patterns.txt > util.txt
timeout 3s bwm-ng -o csv > nw.txt
grep "wlp2s0" nw.txt >> util.txt
rm nw.txt