#!/bin/bash

set -e

for input in ../../data/data.toy/raw/*/Posts.xml
do
  output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
  python strip_posts_to_disk.py $input $output
done
