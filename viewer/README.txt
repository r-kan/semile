=================================================
Utility: viewer for semile
Author: rkan / its_right@msn.com
=================================================

usage: prof_view.py [-h] [-c CONFIG_FILE] profile

The Semile Viewer

positional arguments:
  profile

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        config file name (default: 'config.ini')
-------------------------------------------------
Sample usage:
  python3 prof_view.py case_demo
  => case_demo.png and case_demo.xml will be generated
  
-------------------------------------------------
Configurable options:

[profile]
use_reduced_time (default: False)
  => True: reduce the consumed time of each execution to simulate profiling overhead
  => False: use original consumed time

[view]
longer_time_first (default: False)
  => True: the appearance of execution will be sorted by consumed time
  => False: the appearance of execution will be sorted by its order in profile
 
remove_no_msg_entry (default: False)
  => True: the profile unit without message will not be shown in PNG output

max_branch (default: 10)
  => n: the maximum number of shown inner execution in PNG format output 

max_msg_length (default: 40)
  => n: the maximum length of shown message per execution

=================================================

