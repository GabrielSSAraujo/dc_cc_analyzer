# Pass SRC_DIR as a command line parameter to this makefile
# Example (Windows): mingw32-make all SRC_DIR=project
# Example (Linux): make all SRC_DIR=project

# Compiler and flags
CC=gcc
CFLAGS=

# Source files and output
SRC=$(wildcard $(SRC_DIR)/*.c) # All .c files in the SRC_DIR directory must be in the root
SRC+=modules/coupling_recorder/coupling_recorder.c
SRC+=modules/coupling_recorder/list.c
SRC+=modules/test_driver/c_files/test_driver_sut.c
SRC+=modules/test_driver/c_files/test_driver_suti.c

OBJ=$(SRC:.c=.o)
OBJ_SUT=$(filter-out $(SRC_DIR)/suti.o modules/test_driver/c_files/test_driver_suti.o,$(OBJ))
OBJ_SUTI=$(filter-out $(SRC_DIR)/sut.o modules/test_driver/c_files/test_driver_sut.o,$(OBJ))
OBJ_DIR=objects

# Default rule
all: testdriver_sut testdriver_suti moveObjs
# all: debug

# Linking the target
testdriver_sut: $(OBJ_SUT)
	$(CC) $(CFLAGS) -o $@ $^

testdriver_suti: $(OBJ_SUTI)
	$(CC) $(CFLAGS) -o $@ $^

# Compiling source files into object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

debug:
	@ echo $(SRC)
	@ echo ''
	@ echo $(OBJ_SUT)
	@ echo ''
	@ echo $(OBJ_SUTI)

# REQ-1: A Ferramenta deve executar em sistemas operacionais Windows e distribuições Linux.
# Move
ifeq ($(OS),Windows_NT)
moveObjs:
	@ if not exist $(OBJ_DIR) mkdir $(OBJ_DIR) && move $(SRC_DIR)\*.o $(OBJ_DIR)\ && move modules\test_driver\c_files\*.o $(OBJ_DIR)\ && move modules\coupling_recorder\*.o $(OBJ_DIR)\ 
else
moveObjs:
	@ mkdir -p $(OBJ_DIR) && mv $(SRC_DIR)/*.o modules/test_driver/c_files/*.o modules/coupling_recorder/*.o $(OBJ_DIR)/ 
endif

# Clean up
ifeq ($(OS),Windows_NT)
clean:
	@ rmdir /S /Q $(OBJ_DIR) && del testdriver_sut.exe && del testdriver_suti.exe
else
clean:
	@ rm -rf $(OBJ_DIR) && rm testdriver_sut testdriver_suti
endif

# Dependency rule
.PHONY: all clean
