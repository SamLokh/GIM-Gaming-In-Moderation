# GIM-Gaming-In-Moderation
This program basically enables you to blacklist certain softwares on Windows inorder to limit their usage/screentime. For example, suppose there is this game you want to play, but you wish to do so in moderation, i.e., limit you game time, than you can add that game to this software and this software will continuously monitor the system if that game process becomes active and after the allocated time runs out, it terminates the game process. Basically a productivity program.

Storing the data in MySQL database. Will share the database schema shortly.

**:
Use the GetProcName.py to add a software process that you want to use in limit, in moderation.
The program will begin its countdown of the allocated time once a blacklisted software process becomes active and once it hits zero, the software process will be terminated.
GIM_0_2.py is the main program.

You can use the Windows Task Schedular to run this program after you login and the program will than constantly monitor the system if a blacklisted software becomes active.
