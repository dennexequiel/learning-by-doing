argument1=$1
argument2=$2
argument3=$3
regex='^[0-9]+$'

if [[ $# -eq 0 ]]
    then 
        echo "No arguments were passed!"
elif [[ $# -lt 3 ]]
    then 
        echo "Three arguments are required!"
else
    if [[ -z $argument1 ]] || [[ -z $argument2 ]] || [[ -z $argument3 ]]
        then 
            echo "An argument cannot be an empty string!"
    else
        if [[ $argument1 =~ $regex ]] && [[ $argument2 =~ $regex ]] && [[ $argument3 =~ $regex ]]
            then
                if (( argument1 >= 0 && argument1 <= 7 )) &&
                    (( argument2 >= 0 && argument2 <= 7 )) &&
                    (( argument3 >= 0 && argument3 <= 7 ))
                    then
                        echo "Please enter your name:"
                        read name

                        echo "Please enter the directory name:"
                        read dirName

                        echo "Please enter the file name:"
                        read fileName

                        mkdir -p $dirName
                        cd $dirName
                        touch $fileName
                        echo "Hi $name this is your file." >> $fileName
                        chmod $argument1$argument2$argument3 $fileName 
                        clear

                        echo "***** End of Program *****"
                        echo "Your Name: $name"
                        echo "Directory Name: $dirName"
                        echo "File Name: $fileName"
                        echo "File Content: $(cat $fileName)"
                        echo "Directoy List with Permission: $(ls -l)"
                else
                    echo "One of the arguments exceeded the value of 7!"
                fi
        else
            echo "One of the arguments is not a positive integer!"
        fi    
    fi
fi    