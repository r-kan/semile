# Command line usage
```
usage: smview [-h] [-c CONFIG_FILE] profile

The Semile Viewer

positional arguments:
  profile

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        config file name (default: 'config.ini')
```

# Example
  _python_ **smview** `case_demo`  
  => `case_demo.png` and `case_demo.xml` will be generated  
  
  Note: only support python version 3.x, python version 2.x is not supported  
  
# Configurable file options 

**[profile]**  
`use_reduced_time`=True|False (default: False)  
* True: reduce the consumed time of each execution to simulate profiling overhead  
* False: use original consumed time  
  
**[view]**  
`longer_time_first`=True|False (default: False)  
* True: the appearance of execution will be sorted by consumed time  
* False: the appearance of execution will be sorted by its order in profile  
   
`remove_no_msg_entry`=True|False (default: False)  
* True: the profile unit without message will not be shown in PNG output  
  
`max_branch`=n (default: 10)  
* n: the maximum number of shown inner execution in PNG format output   
  
`max_msg_length`=n (default: 100)  
* n: the maximum length of shown message per execution  
