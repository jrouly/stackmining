"""
Author: Michel Rouly
Date:   2014-04-28
"""


import os
import sys
import time
import random
import logging

import numpy

from s3file import s3open

from collections import Counter

from lxml import etree
from lxml.html import document_fromstring

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline



# Vectorize Data {{{
def vectorize_data(in_protocol="disk",
                   data_dir=".",
                   s3_url="http://cs484project.s3.amazonaws.com",
                   s3_index_file="s3_index_toy.txt",
                   post_file="Posts.xml" ):
    """
    Vectorize Data: read in all Posts.xml files from a directory of
    directories, ie. the main data dump directory. Read entire dataset into
    memory, then perform TF-IDF vectorization and clean the data further.

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


    # Set up empty data stores
    posts = []      # store plain post data
    labels = []     # list of labels, corresponds to each post


    # Store Posts function {{{
    def store_posts( fullpath, category ):
        """
        Store the documents in a dictionary based on their category.

            in_file: the input filename to read (for category)
            category: the category (label) of these posts

        """

        # read in the post data and store it in the posts list
        post_data = read_posts( fullpath, protocol=in_protocol )
        posts.extend( post_data )

        # generate an appropriate num of labels for the posts
        num_posts = len( post_data )
        labels.extend( [category] * num_posts )

    # }}}


    # S3 Data {{{
    # Set up an s3 connection for reading the input over an s3 stream.
    if in_protocol == "s3":
        logging.info("Reading from s3 storage.")

        # Read in the index file (since this is s3)
        index_filename = s3_url + "/" + s3_index_file
        index_file = s3open( index_filename )

        for f in index_file.readlines():

            f = f[:-1] # strip out newlines
            fullpath = s3_url + "/" + data_dir + "/" + f + "/" + post_file
            category  = f[ : f.index(".") ]

            # store the vectors in the corpus
            store_posts( fullpath, category )
    # }}}


    # Disk Data {{{
    # Otherwise read from the local disk.
    else:
        logging.info("Reading from disk.")

        # Loop over the contents of the data directory
        for in_file in os.listdir( data_dir ):

            # Regenerate a full reference to the file we're reading in
            fullpath = os.path.join( data_dir, in_file, post_file )
            category  = in_file[ : in_file.index(".") ]

            # store the vectors in the corpus
            store_posts( fullpath, category )
    # }}}


    # create a tf_idf vectorizer machine
    tfidf_vectorizer = TfidfVectorizer(
        input="content",        # will pass input directly
        encoding="ascii",       # use basic ascii encoding
        decode_error="ignore",  # ignore decoding errors
        strip_accents="ascii",  # strip fancy characters
        stop_words="english",   # remove english stopwords
        lowercase=True,         # lowercase everything
        max_df=0.95,            # terms must occur in under X documents
        min_df=50,              # terms must occur in at least X documents
        use_idf=True,           # inverse document frequency (weighting)
        smooth_idf=True,        # smooth the data out
    )


    # remove HTML entities and perform stop word removal
    logging.info("Vectorizing dataset.")
    vectorized_posts = tfidf_vectorizer.fit_transform( posts )

    logging.info("Data vectorized.")
    logging.debug("Number of entries:    %d." % vectorized_posts.shape[0])
    logging.debug("Number of features:   %d." % vectorized_posts.shape[1])
    logging.debug("Number of categories: %d." % len( set( labels ) ) )


    return (labels, vectorized_posts)
# }}}



# Read Posts {{{
def read_posts( in_file, protocol="disk", sample=200 ):
    """
    Read Posts: read in data from file, parse the XML and spit the cleaned
    output back in an array.

        in_file:  read in from a Posts.xml file
        protocol: [s3|disk]
        sample:   max sample size

    In order to clean posts, we remove html tags and (later) perform stop-word
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

    # logging.debug("Vectorizing over input file.")

    # Read in and clean the bodies of the rows.
    posts = []
    for event, element in etree.iterparse( f ):

        # Read in the row
        body = element.get( "Body", u"" )
        body = body.strip()

        # Strip out empty posts before processing
        if len( body ) == 0:
            continue

        # Strip out html

        body = document_fromstring( body )
        body = body.text_content()
        body = body.encode("ascii", "ignore")
        body = body.strip()

        # Strip out empty posts after processing
        if len( body ) == 0:
            continue

        posts.append( body )

        # Only read in at most sample data points. We assume that the posts
        # are in no particularly relevant order, so this simulates uniform
        # random sampling.
        if sample > 0 and len( posts ) >= sample:
            break

    return posts
# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    if len( sys.argv ) != 3:
        logging.error( "Usage: python read_corpus.py [s3|disk] data_dir" )
        sys.exit( 1 )

    in_protocol = sys.argv[1]
    data_dir = sys.argv[2]

    (labels, data) = vectorize_data( in_protocol=in_protocol,
                                         data_dir=data_dir )

    label_counts = Counter( labels )

    logging.debug( "Labels: " + str( label_counts ) )
    logging.debug( "Data: " + str( data.shape ) )

# }}}



