
all: install

install:
	python3 setup.py build_ext
	python3 setup.py install

clean:
	rm -Rf dist build libimgsmlr.egg-info libimgsmlr/libimgsmlr.so.* libimgsmlr/libimgsmlr.so

go_test:
	cd libimgsmlr && make
	GOOS=darwin GOARCH=amd64 CGO_ENABLED=1 go build  -o ./dist/go_test test.go
