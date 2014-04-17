import os
import sys
import time
import logging

import s3file
import lxml.etree as xml
import sklearn as sk
import numpy as np


# turn on logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s ] %(levelname)s: %(message)s')

args = sys.argv
num_args = len( sys.argv )

if( num_args != 4 ):
    logging.error( "Usage: python strip_posts.py [s3|disk] input_file output_dest" )
    exit( 1 )

protocol = sys.argv[1]
in_file = sys.argv[2]
out_dest = sys.argv[3]

print( "Reading from..  %s\nWriting to....  %s" % (in_file, out_dest) )

if protocol == "disk":
    # create output paths directory if it doesn't already exist
    if not os.path.exists( out_dest ):
        time.sleep( 1 ) # naively avoid race conditions
        os.makedirs( out_dest )

# construct tree over xml data
tree = xml.parse( in_file )
rows = tree.iter("row")

# for each row, split out its contents and output
rownum = 0
for row in rows:

    # generate new filename and contents
    rownum = rownum + 1
    filename = os.path.join( out_dest, "post" + str(rownum) )
    body = row.get("Body").encode("ascii", "ignore")

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
