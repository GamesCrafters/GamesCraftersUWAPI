CC=gcc
CFLAGS=-Iinclude -I../plugin/include
BIN=bin

$(BIN)/libUWAPI.so: create_directories include/*.h src/*.c
	$(CC) $(CFLAGS) -fpic -shared -o libUWAPI.so \
		src/UWAPI_boardstrings_R.c \
		src/UWAPI_boardstrings_C.c \
		src/UWAPI_boardstrings.c \
		src/UWAPI_helpers.c
	mv -f libUWAPI.so $(BIN)/libUWAPI.so

create_directories:
	mkdir -p $(BIN)

clean:
	rm -rf $(BIN)

.PHONY: create_directories clean
