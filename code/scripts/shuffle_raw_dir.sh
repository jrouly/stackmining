#!/bin/bash

set -e

# convert to absolute path, enter directory
raw_directory=$(readlink -m $1)
cd $raw_directory

for dir in *
do

  cd $dir # enter directory
  pwd
  file=Posts.xml

  # remove xml version tag and post tags
  sed -ri '/^.*xml version.*$/d' $file
  sed -ri '/^<\/?posts>/d' $file

  # shuffle lines, overwrite old file with new
  shuf < $file > $file.out
  mv $file.out $file

  # reinsert xml version tag and post tags
  sed -i '1i<\?xml version="1.0" encoding="utf-8"\?>' $file
  sed -i '2i<posts>' $file
  echo "</posts>" >> $file

  cd ..   # leave directory

done
