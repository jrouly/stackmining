#!/bin/bash

set -e

# don't forget final /
s3url="http://cs484project.s3.amazonaws.com/"

for input in ../../data/data.toy/raw/*/Posts.xml
do
  outdir=$( echo $input | sed 's/^.*raw\//posts\//' | sed 's/Posts.xml//' )
  outurl="$s3url$outdir"
  python strip_posts_to_s3.py $input $outurl
done
