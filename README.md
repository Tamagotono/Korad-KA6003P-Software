Korad-KA6003P-Software
======================

Software to control the Korad KA6003p / KA3005p power supplies. Should work with other models too.

I could not find any software to control my KA6003p and KA3005p power supplies under Linux, so I decided to write one.

This is my first program written in Python 3.4 (or any version for that matter) so I am sure there will be many poor coding styles and errors. I am learning as I go, so any suggestions are appreciated.


This software is being written for Linux, but should be easy to get working on Windows and to be made compatible with Python2. These are possiblities, but not high on my list of things to do. If anyone wants to fork this project, you are free to do so. Any fixes, pointers, suggestions for this version are greatly appreciated.
Since this is a learning project for me, I will likely do a complete re-write later on, to fix the bad ideas that get implemented along the way.



TODO:
Replicate front panel controls:
 - Set Current
 - Output on/off
 - OVP
 - OCP

Programable change over time (i.e. 0 - 30V in 0.01V steps over 3 hrs)

Logging:
  - Record any voltage or current changes with a timestamp to a file




DONE:
Replicate front panel controls:
 - Set Voltage
 - Output on/off

Display actual voltage and current
Display set voltage and current


Last updated: 13 Oct, 2014
