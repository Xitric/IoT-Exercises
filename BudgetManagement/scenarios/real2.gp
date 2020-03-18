set term pdfcairo
set output "real2.pdf"

set datafile separator ","
set xrange [:11208]

plot 'real2.csv' using ($1):($2) with lines notitle
