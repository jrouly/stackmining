import os
import sys
import time
import logging

import s3file
import numpy

from lxml.etree import parse
from lxml.html import document_fromstring

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


def vectorize_posts(in_file, out_dest="null", protocol="null"):

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    # catch edge case ouput protocols
    if out_dest == "null" or protocol == "null" or protocol not in ["s3", "disk", "null"]:

        protocol = "null"
        out_dest = "null"

    logging.info( "Reading from..  %s" % in_file )
    logging.info( "Writing to....  %s" % out_dest )

    if protocol == "disk":
        # create output paths directory if it doesn't already exist
        if not os.path.exists( out_dest ):
            time.sleep( 1 ) # naively avoid race conditions
            os.makedirs( out_dest )

    # construct tree over xml data
    tree = parse( in_file )
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
    rownum = 0
    for row in rows:

        # generate new filename and contents
        rownum = rownum + 1
        filename = os.path.join( out_dest, "post" + str(rownum) )
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

        # write body of post to file
        if protocol == "disk":
            row_file = open( filename, 'w' )
            row_file.write( body )
            row_file.close()

        # write body of post out to s3 bucket
        elif protocol == "s3":
            s3 = s3file.s3open( filename )
            s3.write( body )
            s3.close()

        else:
            pass

    # remove HTML entities and perform stop word removal
    vectorized_posts = tfidf_vectorizer.fit_transform( posts )

    return vectorized_posts
