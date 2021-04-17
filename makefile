all: ibus-table-cuneiform.txt
	ibus-table-createdb -s ibus-tables-cuneiform.txt -n cuneiform.db 
	sudo cp cuneiform.db /usr/share/ibus-table/tables/
	sudo cp cuneiform.svg /usr/share/ibus-table/icons/
	ibus-daemon -xrd

ibus-table-cuneiform.txt: ogsl-sl.xml make_ibus_table.py
	./make_ibus_table.py

make_ibus_table.py: make_ibus_table.ipynb
	jupyter nbconvert --to script make_ibus_table.ipynb
	chmod +x make_ibus_table.py

ogsl-sl.xml:
	wget https://github.com/oracc/coredata/blob/master/sign/ogsl-sl.xml?raw=true -O ogsl-sl.xml

clean:
	-rm ibus-tables-cuneiform.txt
	-rm cuneiform.db
	-rm make_ibus_table.py

pretty: ogsl-sl.xml
	xmllint --format ogsl-sl.xml > ogsl-sl_prettified.xml
