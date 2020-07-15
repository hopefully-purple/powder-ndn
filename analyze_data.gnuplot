#GRAPH
#set arguments (title)
TITLE = ARG1

# Set the output to a png file
set terminal png size 1000,800

# The file we'll write the graph to
set output 'plot_timed_data.png'

# The graphic title
set title TITLE

#Move legend
set key outside top

#plot the graphic
#CurrentTime 1  NameTree 2  Fib 3  Pit 4   Measure 5  Cs 6  InInterests 7  OutInterests 8  InData 9  OutData 10  InNack 11  OutNack 12  Satisfied 13  Unsatisfied 14

plot "timed_data.dat" u 1:7 title "InInterests" with lines, "timed_data.dat" u 1:8 title "OutInterests" with lines, "timed_data.dat" u 1:9 title "InData" with lines, "timed_data.dat" u 1:10 title "OutData" with lines, "timed_data.dat" u 1:13 title "SatisfiedInterests" with lines, "timed_data.dat" u 1:14 title "UnsatisfiedInterests" with lines


