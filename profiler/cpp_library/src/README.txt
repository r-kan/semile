=================================================
Utility: cpp library for semantic-profile
Author: rkan / its_right@msn.com
=================================================

Instruction to build the cpp profile library
    make    => Monitor.o will be generated

------------------------------------------------
Instruction to use the cpp profile library in client code
    1. add the location of Monitor.h in compilation
        for example,
            g++ -c -I$(SEMANTIC_PROFILE_HOME)/profiler/cpp_library/src -o client.o client.cpp
    2. add Monitor.o in linking
        for example,
            g++ -o client.o Monitor.o
    3. run the program, then the file 'semantic_profile_CURTIME' will be generated
       (CURTIME: string representation of current datetime)

    Then one can feed the output file to viewer to investigate the profile result

------------------------------------------------
Usage example can be found at $(SEMANTIC_PROFILE_HOME)/profiler/cpp_library/example
=================================================
