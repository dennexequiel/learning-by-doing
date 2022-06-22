## User File Scripting

This script is sample implementation of different bash commands.

## What Does It Do?
1. The user should give three integer numbers as an argument for the
script. (Example: bash userFileScripting.sh 6 4 4).
2. The arguments will serve as the permission to set for the file to be created by the script. These, the are the conditions:
   * The arguments are required or should not be empty. 
   * The argument must be integer value only.
   * The argument must not exceed the value of 7. 
3. If the user gives a valid argument value. The script will ask the user to enter his/her name. 
4. The script will ask the user to enter the name of the directory to be created. 
5. The script will next ask the user to enter the name of the file to be created. 
6. The script should automatically create the directory. Then create the file inside the created
directory. 
7. The script should append the following text inside the file created. Format: Hello <name> this is your file.
8. The script should also set the permissions for the created file base on the arguments given when
running the script.