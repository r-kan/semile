=================================================
Utility: cpp library for semile
Author: rkan / its_right@msn.com
=================================================

Instruction to build the cpp profile library
    make    => Monitor.o will be generated

------------------------------------------------
Instruction to use the cpp profile library in client code
    1. include Monitor.h in source and add its location in compilation
        for example,
            g++ -c -I$(SEMILE_HOME)/profiler/cpp_library/src -o client.o client.cpp
    2. add Monitor.o in linking
        for example,
            g++ -o client.o Monitor.o
    3. run the program, then the file 'semile_CURTIME' will be generated
       (CURTIME: string representation of current datetime)

    Then one can feed the output file to viewer to investigate the profile result

------------------------------------------------
Usage example can be found at $(SEMILE_HOME)/profiler/cpp_library/example
=================================================
