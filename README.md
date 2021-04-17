# ibus-table-cuneiform

An input method to write Sumero-Akkadian cuneiform using IBUS table engine. 
The sign data is from University of Pennsylvania's Oracc project's (http://oracc.museum.upenn.edu/) sign list that can be found here: 
https://github.com/oracc/coredata/blob/master/sign/ogsl-sl.xml .

# Requirements

IBUS, IBUS table, Python3, make. More or less. If you make changes to the Python Notebook, you'll need also Jupyter.
```bash
sudo apt install ibus ibus-table python3 make
```

# Installation

Making the project fetches the sign list, creates the table, installs it into ibus-table's default directory for custom tables, and restarts IBUS.
```bash
make
```

# Usage

After installing and restarting the engine, the input method can be found under language "other".
The input is in ASCII and follows Oracc's conventions (http://oracc.museum.upenn.edu/doc/help/editinginatf/primer/inlinetutorial/index.html).
Long vowels are written by doubling.

ASCII | Unicode
--- | ---
sz/SZ |	š/Š	
s,/S, |	ṣ/Ṣ
t,/T, |	ṭ/Ṭ
s'/S'|	ś/Ś
' |	ʾ 	
0-9 |	₀-₉ 	
x |	 ₓ 
h,/H, |	ḫ/Ḫ
j/J|	ŋ/Ŋ
uu|û'
aa|ā
ee|ē
ii|ī
uu|ū

As expected, sign names are to be written in upper case (and without pipes ('|')), and readings in lower case.
If a reading has multiple candidates, they are differented by the sign name in parenthesis. 
