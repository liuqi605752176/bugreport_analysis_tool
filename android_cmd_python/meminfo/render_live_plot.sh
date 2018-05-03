#!/bin/bash

eog figure.jpg
while [ 1 ] ; 
do 
gnuplot liveplot.gnu
sleep 1

done
