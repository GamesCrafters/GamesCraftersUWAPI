CC=gcc
CFLAGS=-I../include \
	-L../../libUWAPI/bin -lUWAPI \
	-I../../libUWAPI/include

example.so: example.c
	$(CC) $(CFLAGS) -shared -fpic -o example.so example.c

test: example.so
	cp ../../libUWAPI/bin/libUWAPI.so .
	python3 test.py

clean:
	rm -rf *.so

.PHONY: clean
