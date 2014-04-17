#!/bin/bash

set -e


if [ "$2" = "" ]
then
  sourcedir="../../../data/data.toy/raw/"
  echo "No source directory provided. Defaulting to toy dataset: $sourcedir"
else
  sourcedir=$2
fi


# S3 out protocol
if [ "$1" = "s3" ]
then

  # don't forget final /
  s3url="http://cs484project.s3.amazonaws.com/"

  for input in $sourcedir/*/Posts.xml
  do
    outdir=$( echo $input | sed 's/^.*raw\//posts\//' | sed 's/Posts.xml//' )
    outurl="$s3url$outdir"
    python strip_posts.py s3 $input $outurl
  done


# disk out protocol
elif [ "$1" = "disk" ]
then

  for input in $sourcedir/*/Posts.xml
  do
    output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
    python strip_posts.py disk $input $output
  done


else

  echo "No protocol provided. Use 'disk' or 's3'."

fi
