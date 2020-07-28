#Script that analyzes the inout times for router response evaluation

#set arguments (title, req per rep)
TITLE = ARG1
REQS = ARG2

#Set the output to a png file
set terminal png size 1300,800

# Set the file we'll write the graph to
set output 'plot_outin_data.png'

#Set the graphic title
set title TITLE 

#Move legend
set key outside top

set key autotitle columnheader
stats 'results.dat' using 0 nooutput

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

set print 'gnuplotstatistics.txt'
stats 'gnustats.dat' index 0 prefix "A"
unset print
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"
#stats 'results.dat' index 1 prefix "A"

#set label 1 at A_index_max, graph 0.9 "max" center offset 0,1

#Plot with math
#plot [0:REQS] 'results.dat' w linespoints 
plot for [i=0:(STATS_blocks - 1)] 'results.dat' index i w lines 
#plot '1results.dat' index IN w lines
