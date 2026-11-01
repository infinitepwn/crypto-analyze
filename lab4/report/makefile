MAIN=main
OUTDIR=output

.PHONY: all clean cleanall bib

all:
	latexmk -xelatex -output-directory=$(OUTDIR) $(MAIN).tex

clean:
	latexmk -c -output-directory=$(OUTDIR) $(MAIN).tex

cleanall:
	latexmk -C -output-directory=$(OUTDIR) $(MAIN).tex

bib:
	latexmk -xelatex -bibtex -output-directory=$(OUTDIR) $(MAIN).tex
