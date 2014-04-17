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

if( num_args != 3 ):
    logging.error( "Usage: python strip_posts.py input_file output_dir" )
    exit( 1 )

in_file = sys.argv[1]
s3_url = sys.argv[2]

print( "Reading from..  %s\nWriting to....  %s" % (in_file, s3_url) )

# construct tree over xml data
tree = xml.parse( in_file )
rows = tree.iter("row")

# for each row, split out its contents and output
rownum = 0
for row in rows:

    # generate new filename and contents
    rownum = rownum + 1
    filename = os.path.join( s3_url, "post" + str(rownum) )
    body = row.get("Body").encode("ascii", "ignore")

    # write body of post out to s3 bucket
    s3 = s3file.s3open( filename )
    s3.write( body )
    s3.close()
