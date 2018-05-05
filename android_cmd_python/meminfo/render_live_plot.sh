#!/bin/bash
if [ "$1" == "-i" ]; then
    file=liveplot_ion_meminfo.gnu
fi

if [ "$1" == "-m" ]; then
    file=liveplot_meminfo.gnu
fi

if [ "$1" == "-a" ]; then
    file=liveplot_ion_and_meminfo.gnu
fi



while [ 1 ] ; do
gnuplot $file
sleep 1

done
