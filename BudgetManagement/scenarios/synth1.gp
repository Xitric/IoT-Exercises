set term pdfcairo
set output "synth1.pdf"

set datafile separator ","
set xrange [:1440]

plot 'synth1.csv' using ($1):($2) with lines notitle
