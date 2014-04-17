#!/bin/bash

set -e


# S3 out protocol
if [ "$1" = "s3" ]
then

  # don't forget final /
  s3url="http://cs484project.s3.amazonaws.com/"

  for input in ../../data/data.toy/raw/*/Posts.xml
  do
    outdir=$( echo $input | sed 's/^.*raw\//posts\//' | sed 's/Posts.xml//' )
    outurl="$s3url$outdir"
    python strip_posts.py $1 $input $outurl
  done

fi



# disk out protocol
if [ "$1" = "disk" ]
then

  for input in ../../data/data.toy/raw/*/Posts.xml
  do
    output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
    python strip_posts.py $1 $input $output
  done

fi
