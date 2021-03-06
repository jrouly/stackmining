"""
Author: Michel Rouly
Date:   2014-05-07
Desc:   Read in an input directory of files and vectorize them into memory.
"""


import os
import sys
import time
import random
import logging
import ConfigParser

import numpy

from s3file import s3open

from collections import Counter

from lxml import etree
from lxml.html import document_fromstring

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline



# Vectorize Data {{{
def vectorize_data( config ):
    """
    Vectorize Data: read in all Posts.xml files from a directory of
    directories, ie. the main data dump directory. Read entire dataset into
    memory, then perform TF-IDF vectorization and clean the data further.

    config: ConfigParser with documented fields

    """

    # Read in necessary config values.
    in_protocol   = config.get("input", "in_protocol")
    data_dir      = config.get("input", "data_dir")
    post_file     = config.get("input", "post_file")

    s3_url        = config.get("input", "s3_url")
    s3_index_file = config.get("input", "s3_index_file")

    max_df   = config.getfloat("tfidf", "max_df")
    min_df     = config.getint("tfidf", "min_df")

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
        post_data = read_posts( fullpath, config )
        posts.extend( post_data )

        # generate an appropriate num of labels for the posts
        num_posts = len( post_data )
        labels.extend( [category] * num_posts )

        logging.debug("Read %d posts from %s." % (num_posts, category) )

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
        use_idf=True,           # inverse document frequency (weighting)
        smooth_idf=True,        # smooth the data out

        max_df=max_df,          # terms must occur in under X documents
        min_df=min_df,          # terms must occur in at least X documents
    )


    # remove HTML entities and perform stop word removal
    logging.info("Vectorizing dataset.")
    vectorized_posts = tfidf_vectorizer.fit_transform( posts )

    logging.info("Data vectorized.")
    logging.info("  Number of entries:    %d." % vectorized_posts.shape[0])
    logging.info("  Number of features:   %d." % vectorized_posts.shape[1])
    logging.info("  Number of categories: %d." % len( set( labels ) ) )


    return (labels, vectorized_posts)
# }}}



# Read Posts {{{
def read_posts( in_file, config ):
    """
    Read Posts: read in data from file, parse the XML and spit the cleaned
    output back in an array.

    config: ConfigParser with documented fields

    In order to clean posts, we remove html tags and (later) perform stop-word
    removal.
    """

    # Read in necessary config values.
    protocol       = config.get("input", "in_protocol")
    sample_size = config.getint("tfidf", "sample_size")

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

        try:
            body = document_fromstring( body )
            body = body.text_content()
            body = body.encode("ascii", "ignore")
            body = body.strip()
        except:
            continue

        # Strip out empty posts after processing
        if len( body ) == 0:
            continue

        posts.append( body )

        # Only read in at most sample data points. We assume that the posts
        # are in no particularly relevant order, so this simulates uniform
        # random sampling.
        if sample_size > 0 and len( posts ) >= sample_size:
            break

    return posts
# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    if len( sys.argv ) != 3:
        logging.error( "Usage: python read_corpus.py [input.ini] [cluster.ini]" )
        sys.exit( 1 )

    # pull in parameters from the command line
    input_file  = sys.argv[1]
    config_file = sys.argv[2]

    # read configuration file
    config = ConfigParser.ConfigParser( allow_no_value=True )
    config.readfp( open( input_file ) )
    config.readfp( open( config_file ) )

    # run vectorization
    (labels, data) = vectorize_data( config )

    # count number of labels
    label_counts = Counter( labels )

    logging.debug( "Labels: " + str( label_counts ) )
    logging.debug( "Data: " + str( data.shape ) )

# }}}



