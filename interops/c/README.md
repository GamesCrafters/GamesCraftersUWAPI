# Interops with C

This directory contains some experimental code for UWAPI to interface with C.

Before starting any local development, go to `libUWAPI` and run `make` to build yourself dynamic library with useful helper functions to format board strings and free allocated memories.

To add a game written in C, please check out an example project at `interface/example`.

The game needs to follow the interface declared at `interface/include/UWAPI_interface.h` and there's really only one entry point for UWAPI to interop with your existing project.

Run `make` to build a dynamic library for the example project, and then you may run `make test` to see some results of Python trying to access the data via the game-variant service in C.
