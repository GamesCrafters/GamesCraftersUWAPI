CC=gcc
CFLAGS=-Iinclude -I../interface/include
BIN=bin

$(BIN)/libUWAPI.so: create_directories include/*.h src/*.c
	$(CC) $(CFLAGS) -Wl,-install_name,libUWAPI.so -shared -o $(BIN)/libUWAPI.so \
		src/UWAPI_boardstrings_R.c \
		src/UWAPI_boardstrings_C.c \
		src/UWAPI_boardstrings.c \
		src/UWAPI_helpers.c

create_directories:
	mkdir -p $(BIN)

clean:
	rm -rf $(BIN)

.PHONY: create_directories clean
