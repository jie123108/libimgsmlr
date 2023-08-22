
all: install

install:
	python3 setup.py build_ext
	python3 setup.py install

upload_pypi:
	python3 setup.py sdist
	python3 -m pip install twine
	twine upload dist/*
clean:
	rm -Rf dist build libimgsmlr.egg-info libimgsmlr/libimgsmlr.so.* libimgsmlr/libimgsmlr.so
