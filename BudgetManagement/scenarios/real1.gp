set term pdfcairo
set output "real1.pdf"

set datafile separator ","
set xrange [:6580]

plot 'real1.csv' using ($1):($2) with lines notitle
