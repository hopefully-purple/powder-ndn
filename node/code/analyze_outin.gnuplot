#Script that analyzes the inout times for router response evaluation

#set arguments (title, req per rep)
TITLE = ARG1
REQS = ARG2

#Set the output to a png file
set terminal png size 1300,800

# Set the file we'll write the graph to
set output 'data_collection/plot_outin_data.png'

#Set the graphic title
set title TITLE 

#Move legend
set key outside top

set key autotitle columnheader
stats 'data_collection/results.dat' using 0 nooutput

set xlabel "Number of Requests"
set ylabel "Router Response time (seconds)"

if (REQS > 30) {
	set autoscale x
} else {
	#Set the x and y ranges
	set xrange [0:REQS - 1]
	#set yrange [10000:13000]
	set xtics 1
}
set grid

set print 'data_collection/gnuplotstatistics.txt'
stats 'data_collection/gnustats.dat' index 0 prefix "A"
unset print

#Plot with math
plot for [i=0:(STATS_blocks - 1)] 'data_collection/results.dat' index i w lines 
