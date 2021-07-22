
all: install

install:
	python3 setup.py build_ext
	python3 setup.py install

clean:
	rm -Rf dist build libimgsmlr.egg-info libimgsmlr/libimgsmlr.so.* libimgsmlr/libimgsmlr.so
