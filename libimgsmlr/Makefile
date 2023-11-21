# imgsmlr/Makefile

CC=gcc
MYCFLAGS=-g -Werror -fPIC
MYLDFLAGS=-lgd

SRCS=imgsmlr.c

all: libimgsmlr.so libimgsmlr.$(shell uname).a

libimgsmlr.so: ${SRCS}
	$(CC) ${MYCFLAGS} ${MYLDFLAGS} -Werror $^ -shared -o $@

libimgsmlr.$(shell uname).a: ${SRCS}
	$(CC) ${CFLAGS_A} -c $^
	ar rc $@ *.o
	rm -f *.o

clean:
	rm -f libimgsmlr.so libimgsmlr.*.a