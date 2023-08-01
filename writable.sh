#We land in a share with a lot of folders, out of which some might be writable. A small bash script
#can determine this.
#!/bin/bash
list=$(find /mnt -type d)
for d in $list
do
    touch $d/x 2>/dev/null
    if [ $? -eq 0 ]
    then
            echo $d " is writable"
    fi
done
