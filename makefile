# Makefile
# Use: make all pd=<pd>
# Where <pd> is the path to the project directory to be compiled

# Name of the project
PROJ_NAME=testdriver

# Source .c files
# C_SOURCE=$(shell find $(pd) -name '*.c' -not -name 'main.c' -not -name 'SUT.c' -not -name 'suti.c')

TESTDRIVER_SUT=./modules/test_driver/c_files/test_driver_sut.c
TESTDRIVER_SUTI=./modules/test_driver/c_files/test_driver_suti.c
COUPLING_RECORDER=./modules/coupling_recorder

# Object files
# OBJ=$(patsubst %.c,%.o,$(C_SOURCE))

# Compiler
CC=gcc

# Flags
CC_FLAGS=-c -Wall

# Clean command
RM=rm -rf

# Compilation and linking
all: testdriver_sut testdriver_suti moveObjsToDirectory

# $(PROJ_NAME): $(OBJ)
# 	$(CC) -o $@ $^ -o $@

testdriver_sut: $(OBJ) test_driver_sut.o list.o coupling_recorder.o $(pd)/sut.o
	$(CC) -o $@ $^ -o $@

testdriver_suti: $(OBJ) test_driver_suti.o list.o coupling_recorder.o $(pd)/suti.o
	$(CC) -o $@ $^ -o $@

# %.o: %.c
# 	$(CC) -o $@ $(CC_FLAGS) $<

test_driver_sut.o: $(TESTDRIVER_SUT)
	$(CC) -o $@ $(CC_FLAGS) $<

test_driver_suti.o: $(TESTDRIVER_SUTI)
	$(CC) -o $@ $(CC_FLAGS) $<

$(pd)/sut.o: $(pd)/SUT.c
	$(CC) -o $@ $(CC_FLAGS) $<

$(pd)/suti.o: $(pd)/suti.c
	$(CC) -o $@ $(CC_FLAGS) $<

list.o: $(COUPLING_RECORDER)/list.c
	$(CC) -o $@ $(CC_FLAGS) $<

coupling_recorder.o: $(COUPLING_RECORDER)/coupling_recorder.c list.o 
	$(CC) -o $@ $(CC_FLAGS) $<

# Avoid polluting the original project
moveObjsToDirectory:
	@ mkdir -p objects
	@ mv test_driver_sut.o test_driver_suti.o objects
	@ mv $(pd)/sut.o $(pd)/suti.o coupling_recorder.o list.o objects

clean:
	@ $(RM) objects testdriver_sut testdriver_suti *~

# Avoid conflicts with keywords 'all' and 'clean'
.PHONY: all clean