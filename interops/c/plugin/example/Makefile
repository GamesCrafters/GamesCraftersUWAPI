CC=gcc
CFLAGS=-I../include \
	-I../../libUWAPI/include -L../../libUWAPI/bin

example.so: example.c
	$(CC) $(CFLAGS) -shared -fpic -o example.so example.c -lUWAPI

test: example.so
	cp ../../libUWAPI/bin/libUWAPI.so .
	LD_LIBRARY_PATH=. python3 test.py

clean:
	rm -rf *.so

.PHONY: clean
