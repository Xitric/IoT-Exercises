set term pdfcairo
set output "synth3.pdf"

set datafile separator ","
set xrange [:1440]

plot 'synth3.csv' using ($1):($2) with lines notitle
