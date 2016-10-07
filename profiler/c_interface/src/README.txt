=================================================
Utility: c interface for semile
Author: rkan / its_right@msn.com
=================================================

Instruction to build the c profile interface
    1. build the cpp profile library (check <SEMILE_HOME>/profiler/cpp_library/src/README.txt)
    2. make    => Monitor_c.o will be generated

------------------------------------------------
Instruction to use the c profile interface in client code
    1. include Monitor_c.h in source and add its location in compilation
        for example,
            gcc -c -I$(SEMILE_HOME)/profiler/c_interface/src -o client.o client.c
    2. add Monitor.o, and Monitor_c.o in linking
        for example,
            g++ -o a.out main.o client.o Monitor.o Monitor_c.o
    3. run the program, then the file 'semile_CURTIME' will be generated
       (CURTIME: string representation of current datetime)

    Then one can feed the output file to viewer to investigate the profile result

------------------------------------------------
Usage example can be found at $(SEMILE_HOME)/profiler/c_interface/example
=================================================
