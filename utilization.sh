if [ -f "util.txt" ] ; then
    echo "Removing previous utilization output"
    rm "util.txt"
fi
top -b -n3  | grep -f patterns.txt > util.txt
echo "CPU charecteristics taken"
timeout 3s bwm-ng -o csv > nw.txt
grep -f patterns.txt nw.txt >> util.txt
echo "Network charecteristics taken"
rm nw.txt
