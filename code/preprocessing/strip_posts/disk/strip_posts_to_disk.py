import os
import sys
import time
import logging

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
out_dir = sys.argv[2]

print( "Reading from..  %s\nWriting to....  %s" % (in_file, out_dir) )

# create output paths directory if it doesn't already exist
if not os.path.exists( out_dir ):
    time.sleep( 1 ) # naively avoid race conditions
    os.makedirs( out_dir )

# construct tree over xml data
tree = xml.parse( in_file )
rows = tree.iter("row")

# for each row, split out its contents and output
rownum = 0
for row in rows:

    # generate new filename and contents
    rownum = rownum + 1
    filename = os.path.join( out_dir, "post" + str(rownum) )
    body = row.get("Body").encode("ascii", "ignore")

    # write body of post to file
    row_file = open( filename, 'w' )
    row_file.write( body )
    row_file.close()
