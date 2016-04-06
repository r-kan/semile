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
  => prof_view.png and prof_view.xml will be generated
  
-------------------------------------------------
Configurable options:

[profile]
use_reduced_time
  => True: reduce the consumed time of each execution to simulate profiling overhead
  => False: use original consumed time

[view]
longer_time_first
  => True: the appearance of execution will be sorted by consumed time
  => False: the appearance of execution will be sorted by its order in profile
  
max_branch
  => n: the maximum number of shown inner execution in PNG format output 

max_msg_length:
  => n: the maximum length of shown message per execution

=================================================

