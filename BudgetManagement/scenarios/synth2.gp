set term pdfcairo
set output "synth2.pdf"

set datafile separator ","
set xrange [:1440]

plot 'synth2.csv' using ($1):($2) with lines notitle
