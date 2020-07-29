#GRAPH
#set arguments (title)
TITLE = ARG1
INTERVAL = ARG2
# Set the output to a png file
set terminal png size 1300,800

# The file we'll write the graph to
set output 'data_collection/plot_timed_data.png'

# The graphic title
set title TITLE
set xlabel "Time"
set ylabel "Entries"
#Move legend
set key outside top

#set xtics 1 
set grid

#plot the graphic
#CurrentTime 1  NameTree 2  Fib 3  Pit 4   Measure 5  Cs 6  InInterests 7  OutInterests 8  InData 9  OutData 10  InNack 11  OutNack 12  Satisfied 13  Unsatisfied 14

#plot [0:999000] 'timed_data.dat' u 1:9 title "InData" w linespoints
#plot 'timed_data.dat' u 1:13 w linespoints
plot "data_collection/timed_data.dat" u 1:3 title "FIB" w linespoints, \
	"data_collection/timed_data.dat" u 1:4 title "PIT" w linespoints lw 3, \
	"data_collection/timed_data.dat" u 1:6 title "ContentStore" w linespoints lw 3, \
	"data_collection/timed_data.dat" u 1:7 title "InInterests" with linespoints, \
	"data_collection/timed_data.dat" u 1:8 title "OutInterests" with linespoints, \
	"data_collection/timed_data.dat" u 1:9 title "InData" with linespoints, \
	"data_collection/timed_data.dat" u 1:10 title "OutData" with linespoints, \
	"data_collection/timed_data.dat" u 1:11 title "InNack" w linespoints, \
	"data_collection/timed_data.dat" u 1:12 title "OutNack" w linespoints, \
	"data_collection/timed_data.dat" u 1:13 title "SatisfiedInterests" with linespoints lw 3, \
	"data_collection/timed_data.dat" u 1:14 title "UnsatisfiedInterests" with linespoints lw 3


