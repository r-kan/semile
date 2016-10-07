# compiler settings
CXX		= g++
DEBUG		= -g
OPT		= -O3
CXXFLAGS	= -std=c++11 -fPIC -m64 -pipe -Wall -W -D_REENTRANT $(OPT)
LFLAGS		= 
SEMILE_INC      = ../../cpp_library/src
SRC_FILES	= Monitor_c.cpp
OBJ_FILES	= $(SRC_FILES:.cpp=.o)

# implicit rules
.cpp.o:
	@echo  "\033[036m  compile "$<" \033[0m" 
	@$(CXX) -c $(CXXFLAGS) -I$(SEMILE_INC) -o "$@" "$<"

all:	$(OBJ_FILES)

# ordinary make rules
clean:
	@echo  "\033[036m  clean all \033[0m" 
	@rm -f $(OBJ_FILES)

