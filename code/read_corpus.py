"""
Author: Michel Rouly
Date:   2014-04-24
"""


import os
import sys
import time
import logging

import numpy

from s3file import s3open

from lxml.etree import parse
from lxml.html import document_fromstring

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


def read_corpus(in_protocol="disk",
                data_dir=".",
                s3_url="http://cs484project.s3.amazonaws.com",
                s3_index_file="index.txt",
                post_file="Posts.xml" ):
    """
    Read Posts: read in Posts.xml files from a directory of directories,
    ie. the main data dump directory.

        in_protocol: [s3|disk]
        data_dir:    input directory, defaults to cwd
        s3_url:      ignored if protocol is disk
        s3_index_file: ignored if protocol is disk
        post_file:   name of data files, defaults to Posts.xml

    """

    # Verify that we have a valid input protocol, default to disk.
    if in_protocol not in ["s3", "disk"]:
        logging.error("Invalid input protocol.")
        sys.exit(1)

    # Set up an empty corpus
    corpus = {}

    # Set up an s3 connection for reading the input over an s3 stream.
    if in_protocol == "s3":
        logging.info("Reading from s3 storage.")

        # Read in the index file (since this is s3)
        index_filename = s3_url + "/" + s3_index_file
        index_file = s3open( index_filename )

        for f in index_file.readlines():

            f = f[:-1] # strip out newlines
            fullpath = s3_url + "/" + data_dir + "/" + f + "/" + post_file

            # Store the vectorized documents based on their category
            category = f[ : f.index(".") ]
            vectors = vectorize_file( fullpath, protocol=in_protocol )
            corpus[category] = vectors

    # Otherwise read from the local disk.
    else:
        logging.info("Reading from disk.")

        # Loop over the contents of the data directory
        for in_file in os.listdir( data_dir ):

            # Regenerate a full reference to the file we're reading in
            fullpath = os.path.join( data_dir, in_file, post_file )

            # Store the vectorized documents based on their category
            category = in_file[ : in_file.index(".") ]
            vectors = vectorize_file( fullpath, protocol=in_protocol )
            corpus[category] = vectors

    logging.info("Corpus vectorized.")
    return corpus



def vectorize_file( in_file, protocol="disk" ):
    """
    Vectorize Category: read in, clean, and represent post data as a numpy
    sparse tf-idf array.

        in_file: read in from a Posts.xml file
        protocol: [s3|disk]

    In order to clean posts, we remove html tags and perform stop-word
    removal.
    """

    # Verify that we have a valid input protocol, default to disk.
    if protocol not in ["s3", "disk"]:
        logging.error("Invalid input protocol.")
        sys.exit(1)

    f = None # empty file handle

    # Reading in from an s3 bucket
    if protocol == "s3":
        f = s3open( in_file )

    # Reading in from local disk storage
    else:
        f = open( in_file, 'r' )

    logging.info("Vectorizing over input file.")

    # construct tree over xml data
    tree = parse( f )
    f.close()
    rows = tree.iter("row")

    # create a tf_idf vectorizer machine
    tfidf_vectorizer = TfidfVectorizer(
        input="content",
        encoding="ascii",
        decode_error="ignore",
        strip_accents="ascii",
        stop_words="english",
        lowercase=True,
        max_df=0.9,
        use_idf=True,
        smooth_idf=True,
    )

    posts = []

    # for each row, split out its contents and output
    for row in rows:

        body = row.get("Body")

        # skip empty documents
        if len( body ) == 0:
            continue

        # strip out html
        body = document_fromstring( body )
        body = body.text_content()
        body = body.encode("ascii", "ignore")

        # add to list in memory
        posts.append( body )

    # remove HTML entities and perform stop word removal
    vectorized_posts = tfidf_vectorizer.fit_transform( posts )

    return vectorized_posts


if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    if len( sys.argv ) != 3:
        logging.error( "Usage: python read_corpus.py [s3|disk] data_dir" )
        sys.exit( 1 )

    in_protocol = sys.argv[1]
    data_dir = sys.argv[2]

    corpus = read_corpus( in_protocol=in_protocol, data_dir=data_dir )
    print( corpus )


