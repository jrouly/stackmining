#!/bin/bash

set -e

# convert to absolute path, enter directory
raw_directory=$(readlink -m $1)
cd $raw_directory

for dir in *
do

  dir=$1
  file=$2

  echo $dir
  file=Posts.xml

  # remove xml version tag and post tags
  sed -ri '/^.*xml version.*$/d' $dir/$file
  sed -ri '/^<\/?posts>/d' $dir/$file

  # shuffle lines, overwrite old file with new
  shuf < $dir/$file > $dir/$file.out
  mv $dir/$file.out $dir/$file

  # reinsert xml version tag and post tags
  sed -i '1i<\?xml version="1.0" encoding="utf-8"\?>' $dir/$file
  sed -i '2i<posts>' $dir/$file
  echo "</posts>" >> $dir/$file

done
