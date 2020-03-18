TARGETS = \
	real1.pdf \
	real2.pdf \
	synth1.pdf \
	synth2.pdf \
	synth3.pdf \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch d~
	rm    *~


%.pdf: %.gp %.csv
	gnuplot $<

