set term pdfcairo
set output "reception.pdf"

set datafile separator ","
set xrange [:1440]

plot 'reception.csv' using ($1):($2) with lines notitle
