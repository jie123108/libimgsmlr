# imgsmlr/Makefile

CC=gcc
CFLAGS=-g -Werror -fPIC
LDFLAGS=-lgd

SRCS=imgsmlr.c

all: libimgsmlr.so libimgsmlr.$(shell uname).a

libimgsmlr.so: ${SRCS}
	$(CC) ${CFLAGS} ${LDFLAGS} -Werror $^ -shared -o $@

libimgsmlr.$(shell uname).a: ${SRCS}
	$(CC) ${CFLAGS_A} -c $^
	ar rc $@ *.o
	rm -f *.o

clean:
	rm -f libimgsmlr.so libimgsmlr.*.a