#!/bin/bash

set -e

for input in ../../data/data/raw/*/Posts.xml
do
  output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
  python strip_posts.py $input $output
done
