
export TEXMFHOME = lsst-texmf/texmf

#for dependency you want all tex files  but for acronyms you do not want to include the acronyms file itself.
tex=$(filter-out $(wildcard *acronyms.tex) , $(wildcard *.tex))  


SRC= LDM-153.tex

OBJ=$(SRC:.tex=.pdf)

#Default when you type make
all: $(OBJ)

$(OBJ): $(tex) core_tables.tex
	latexmk -bibtex -xelatex -f $(SRC)

#core_tables.tex: make_tables.py
#	python3 make_tables.py

#The generateAcronyms.py  script is in lsst-texmf/bin - put that in the path
#acronyms.tex :$(tex) myacronyms.txt
#	lsst-texmf/bin/generateAcronyms.py   $(tex)

clean :
	latexmk -c
	rm *.pdf *.nav *.bbl *.xdv *.snm



