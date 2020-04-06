CC=gcc
CFLAGS=-I../include \
	-L../../libUWAPI/bin -lUWAPI \
	-I../../libUWAPI/include

example: example.c
	$(CC) $(CFLAGS) -shared -o example.so example.c

test:
	cp ../../libUWAPI/bin/libUWAPI.so .
	python3 test.py
