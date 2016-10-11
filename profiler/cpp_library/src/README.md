# Instruction to build the cpp profile library  
_make_    => `Monitor.o` will be generated  

# Instruction to use the cpp profile library in client code  
1. include `Monitor.h` in source and add its location in compilation, for example,  
        _g++ -c -I$(SEMILE_HOME)/profiler/cpp_library/src -o client.o client.cpp_  
2. add `Monitor.o` in linking, for example,  
        _g++ -o a.out main.o client.o Monitor.o_  
3. run the program, then the file `semile_CURTIME` will be generated  
   (CURTIME: string representation of current datetime)  

Then one can feed the output file to viewer to investigate the profile result  

###

Usage example can be found at <a href='https://github.com/r-kan/semile/tree/master/profiler/cpp_library/example'>cpp_library/example</a>
