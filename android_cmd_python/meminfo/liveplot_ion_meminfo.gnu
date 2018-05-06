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
set yrange [0:3145728]
#set yrange [0:131072]

set title "SDM450 RAM Usage"
set key reverse Left outside
set grid

#set terminal jpeg size 1600, 900
set terminal jpeg size 2048, 1080

set size 1,1
set output "figure_ion_meminfo.jpg"
set style data line

plot "dump_ion_meminfo.txt" u 1:2 t "ion mem Total", \


pause 1
reread
