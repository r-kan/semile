# semile :)
_~Simpler way to profile and diagnose~_ http://r-kan.github.io/semile/  
Update: `semile` is refined with much more simpler use model! 

#What is _semile_?  
A profiling framework provides the ability to monitor programs, in general of any programming language, by the following two pieces of information:  
1. consumed time per execution  
2. 'footprint' debug message per execution  

#Difference with other profiling tools?  
* **_Profile 'semantically'_**  Each call to the same function plays its individual role within profiling. Normal 'syntactic' profilers are good in other aspects but fail to achieve this.  
* **_Lightweight_**  The profiled program gives little run-time overhead. The viewer is compact that targets to provide only necessary information without fancy visual effect. It gives profile result in widespread PNG and XML format.  
* **_Message-embedded profile_**  Custom information can be left within profile elements. It then also provides the ability to help reveal internal state/decision inside the program.  

P.S. The user-provided semantic specifications (via the profile library) is necessary for semantic profile  

# System Requirement
python3 (viewer)   
g++ (c/cpp profile library)  

# Dependent Library
<a href="http://www.graphviz.org" target="_blank">dot (graphviz)</a>   

# Use _semile_
<a href="https://github.com/r-kan/semile/tree/master/profiler/cpp_library/src" target="_blank">profiler/cpp_library/src/README.txt</a> => check to see how to use cpp profile library  
<a href="https://github.com/r-kan/semile/tree/master/profiler/cpp_library/example" target="_blank">profiler/cpp_library/example</a> => check to see an example using profile library  
<a href="https://github.com/r-kan/semile/tree/master/viewer" target="_blank">viewer/README.txt</a> => check to see how to use semile viewer

# Contact  
Please contact <a href='http://r-kan.github.io'>*Rodney Kan*</a> by its_right@msn.com for any question/request/bug without hesitation. 

***
Find screenshots, tutorials, and more information at http://r-kan.github.io/semile/!
