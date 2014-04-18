#!/bin/bash

set -e


if [ "$2" = "" ]
then
  echo "No source directory provided."
  exit 1
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
    python -c "from vectorize.vectorize_posts import vectorize_posts;
vectorize_posts( \"$input\", out_dest=\"$outurl\", protocol=\"s3\" );"
  done


# disk out protocol
elif [ "$1" = "disk" ]
then

  for input in $sourcedir/*/Posts.xml
  do
    output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
    python -c "from vectorize.vectorize_posts import vectorize_posts;
vectorize_posts( \"$input\", out_dest=\"$output\", protocol=\"disk\" );"
  done


# null output protocol
elif [ "$1" = "null" ]
then

  for input in $sourcedir/*/Posts.xml
  do
    output=$( echo $input | sed 's/raw/posts/' | sed 's/Posts.xml//' )
    python -c "from vectorize.vectorize_posts import vectorize_posts;
vectorize_posts( \"$input\" );"
  done


# no output protocol given
else

  echo "No protocol provided. Use 'disk' or 's3'."
  exit 1

fi
