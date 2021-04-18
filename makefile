package_name=ibus-tables-cuneiform_1.1.0_all

install: cuneiform.db
	sudo cp cuneiform.db /usr/share/ibus-table/tables/
	sudo cp cuneiform.svg /usr/share/ibus-table/icons/
	ibus-daemon -xrd
	
cuneiform.db: ibus-table-cuneiform.txt
	ibus-table-createdb -s ibus-tables-cuneiform.txt -n cuneiform.db 

#ibus-table-cuneiform.txt: ogsl-sl.xml xml2ibus_table.py
#	./xml2ibus_table.py

ibus-table-cuneiform.txt: ogsl.asl asl2ibus_table.py
	./asl2ibus_table.py

asl2ibus_table.py: asl2ibus_table.ipynb
	jupyter nbconvert --to script asl2ibus_table.ipynb
	chmod +x asl2ibus_table.py

xml2ibus_table.py: xml2ibus_table.ipynb
	jupyter nbconvert --to script xml2ibus_table.ipynb
	chmod +x xml2ibus_table.py


ogsl.asl:
	wget https://raw.githubusercontent.com/oracc/ogsl/master/00lib/ogsl.asl
ogsl-sl.xml:
	wget https://github.com/oracc/coredata/blob/master/sign/ogsl-sl.xml?raw=true -O ogsl-sl.xml

clean:
	-rm ibus-tables-cuneiform.txt
	-rm cuneiform.db
	-rm xml2ibus_table.py
	-rm -r $(package_name)

pretty: ogsl-sl.xml
	xmllint --format ogsl-sl.xml > ogsl-sl_prettified.xml

deb: cuneiform.db
	mkdir -p $(package_name)/usr/share/ibus-table/tables/
	mkdir -p $(package_name)/usr/share/ibus-table/icons/
	mkdir -p $(package_name)/DEBIAN/
	cp cuneiform.db $(package_name)/usr/share/ibus-table/tables/
	cp cuneiform.svg $(package_name)/usr/share/ibus-table/icons/
	cp deb/control $(package_name)/DEBIAN/
	dpkg-deb --build $(package_name)
	
