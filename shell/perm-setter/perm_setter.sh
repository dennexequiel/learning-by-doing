#!/bin/bash
# Script to create a file with specific permissions based on command line arguments

# Get arguments (assumed to be octal permission digits)
argument1=$1
argument2=$2
argument3=$3

# Regular expression to match only numeric characters
regex='^[0-9]+$' 

# Check for no arguments passed
if [[ $# -eq 0 ]]
then 
    echo "No arguments were passed!"

# Check if less than three arguments passed
elif [[ $# -lt 3 ]]
then 
    echo "Three arguments are required!"

# Check if any argument is empty
else
    if [[ -z $argument1 ]] || [[ -z $argument2 ]] || [[ -z $argument3 ]]
    then 
        echo "An argument cannot be an empty string!"

    # Check if all arguments are positive integers
    else
        if [[ $argument1 =~ $regex ]] && [[ $argument2 =~ $regex ]] && [[ $argument3 =~ $regex ]]
        then
            # Check if each argument is between 0 and 7 (octal range)
            if (( argument1 >= 0 && argument1 <= 7 )) &&
               (( argument2 >= 0 && argument2 <= 7 )) &&
               (( argument3 >= 0 && argument3 <= 7 ))
            then
                # Input user information
                echo "Please enter your name:"
                read name

                echo "Please enter the directory name:"
                read dirName

                echo "Please enter the file name:"
                read fileName

                # Create directory and file
                mkdir -p $dirName
                cd $dirName
                touch $fileName
                echo "Hi $name this is your file." >> $fileName

                # Set file permissions
                chmod $argument1$argument2$argument3 $fileName 
                clear

                # Display program summary
                echo "***** End of Program *****"
                echo "Your Name: $name"
                echo "Directory Name: $dirName"
                echo "File Name: $fileName"
                echo "File Content: $(cat $fileName)"
                echo "Directory List with Permission: $(ls -l)"

            else
                echo "One of the arguments exceeded the value of 7!"
            fi

        else
            echo "One of the arguments is not a positive integer!"
        fi
    fi
fi