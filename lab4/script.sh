#!/bin/bash

file=hash.txt

if [ -f file ]
then
    cat > $file
else
    touch $file
fi

cat personal.txt | md5sum >> hash.txt
cat personal.txt | sha1sum >> hash.txt
cat personal.txt | sha224sum >> hash.txt
cat personal.txt | sha256sum >> hash.txt
cat personal.txt | sha384sum >> hash.txt
cat personal.txt | sha512sum >> hash.txt