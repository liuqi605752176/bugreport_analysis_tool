reset
set terminal png
set xdata time
set timefmt "%d-%m-%Y_%H-%M-%S"
set format x "%H-%M-%S"
set xlabel "Time M:S"
set format y "%.f"
set ylabel "Memory in KB"

#set yrange [0:525288]
#set yrange [0:262144]
set yrange [0:3000]
#set yrange [0:131072]

set title "FD leak"
set key reverse Left outside
set grid

#set terminal jpeg size 1600, 900
set terminal jpeg size 2048, 1080

set size 1,1
set output "figure_fd_leak.jpg"
set style data line

plot "fd_leak.txt" u 1:2 t "Open Fd", \


pause 1
reread

