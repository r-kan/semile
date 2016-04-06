MONITOR_LIB   = ../src/Monitor.o
MONITOR_INC   = ../src/

# compiler settings
CXX		= g++
DEBUG		= -g
OPT		= -O3
CXXFLAGS	= -std=c++11 -fPIC -m64 -pipe -Wall -W -D_REENTRANT $(OPT)
LFLAGS		= 

BIN		= run_quicksort
SRC_FILES	= main.cpp quicksort.cpp
OBJ_FILES	= $(SRC_FILES:.cpp=.o)

# 1st (starting) make rule 
all: $(BIN)

# implicit rules
.cpp.o:
	@echo  "\033[036m  compile "$<" \033[0m" 
	@$(CXX) -c $(CXXFLAGS) -I$(MONITOR_INC) -o "$@" "$<"

# ordinary make rules
clean:
	@echo  "\033[036m  clean all \033[0m" 
	@rm -f $(OBJ_FILES) $(BIN)

run_quicksort: $(OBJ_FILES)
	@$(CXX) $(LFLAGS) -o $@ $^ $(MONITOR_LIB)
	@echo  "\033[036m  make "$@" done :) \033[0m"
