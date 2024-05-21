## File Creation and Permission Setting Script (perm_setter.sh)

This Bash script simplifies the process of creating a file with custom permissions within a specified directory.

### Purpose

The script allows users to quickly generate a file with a personalized greeting and set specific permissions for the file. This is useful for learning about file permissions in Linux/Unix systems and for automating file creation tasks.

### How to Use

1. **Provide Permissions as Arguments:** Run the script from your terminal, providing three octal numbers (0-7) as arguments. These numbers represent the permissions for the file's owner, group, and others, respectively. 
 Example:
   ```bash
   ./perm_setter.sh 6 4 4  # Sets permissions to rw- r-- r--
   ```
   
2. **Input Information:**
   * You'll be asked to enter your name.
   * You'll be asked to enter the name of the directory where the file will be created.
   * You'll be asked to enter the desired name for the new file.

### Functionality

* **Argument Validation:** The script checks that:
    * Three arguments are provided.
    * Each argument is a valid octal number (0-7).
    * No arguments are empty strings.

* **Directory and File Creation:**
    * If the specified directory doesn't exist, it is created.
    * A new file is created within the specified directory.

* **Content and Permissions:**
    * A personalized greeting ("Hi [your name], this is your file.") is added to the file.
    * The file's permissions are set according to the arguments you provided.

* **Output:**
    * The script provides a summary of the operation, including:
        * Your name
        * The directory name
        * The file name
        * The file's content
        * The directory listing with file permissions

### Requirements

* **Bash:** This script is designed to run in a Bash shell environment.

### Additional Notes

* Ensure you have write permissions in the directory where you intend to create the file.
* The script automatically overwrites any existing file with the same name in the specified directory.