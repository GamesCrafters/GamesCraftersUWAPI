# Interops with C

This directory contains some experimental code for UWAPI to interface with C programs.

Before starting any local development, go to `libUWAPI/` and run `make` to build yourself a dynamic library with useful helper functions to format board strings.

To add a game written in C, please check out an example project at `plugin/example/`.

The game needs to follow the plugin interface declared in `plugin/include/UWAPI_plugin.h`, and there's really only one entry point for the Universal Web API server in Python to interact with your existing C program.

In the example project (`plugin/example/`), run `make` to build a dynamic library for the example game, and `make test` to see some results of Python attempting to access the data.
