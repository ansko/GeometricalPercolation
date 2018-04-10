#!/usr/bin/env gnuplot

set terminal png size 1024, 768 font "Helvetica, 20"
set output 'PIC.png'
#set xtics 0.25 nomirror
set xtics nomirror
#set yrange [0 to 0.8]
#set xrange [0 to 0.05]
set ytics nomirror
set pointsize 3

#set ylabel "Interface Volume Content"
#set xlabel 'MMT Volume Content'

set key right bottom

plot 'log' u 1:2 w p pointtype 5 lc rgb "red"
