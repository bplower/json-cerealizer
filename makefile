install:
	pip install .

uninstall:
	pip uninstall -y json-cerealizer

reinstall: uninstall install

test:
	nosetests tests/
