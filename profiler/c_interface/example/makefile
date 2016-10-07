CINTF_LIB   = ../src/Monitor_c.o
CINTF_INC   = ../src/
SEMILE_LIB      = ../../cpp_library/src/Monitor.o

# compiler settings
C		= gcc
CXX		= g++
DEBUG		= -g
OPT		= -O3
CFLAGS	        = -fPIC -m64 -pipe -Wall -W -D_REENTRANT $(OPT)
LFLAGS		= 
BIN		= run_quicksort
SRC_FILES	= main.c quicksort.c
OBJ_FILES	= $(SRC_FILES:.c=.o)

# 1st (starting) make rule 
all: $(BIN)

# implicit rules
.c.o:
	@echo  "\033[036m  compile "$<" \033[0m" 
	@$(C) -c $(CFLAGS) -I$(CINTF_INC) -o "$@" "$<"

# ordinary make rules
clean:
	@echo  "\033[036m  clean all \033[0m" 
	@rm -f $(OBJ_FILES) $(BIN)

run_quicksort: $(OBJ_FILES)
	@$(CXX) $(LFLAGS) -o $@ $^ $(SEMILE_LIB) $(CINTF_LIB)
	@echo  "\033[036m  make "$@" done :) \033[0m"
