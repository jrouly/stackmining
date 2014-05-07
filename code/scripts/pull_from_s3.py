"""
Author: Michel Rouly
Date:   2014-05-07
Desc:   Small, hackish script to sequentially pull files on s3 pointed to
        by an index file into a local directory.
"""


import os
import sys
import logging
from s3file import s3open



# Read Posts {{{
def pull_from_s3( s3_url, s3_index_file, output_dir ):
    """
    Pull From s3: copy data from an S3 bucket given an index file.

    s3_url:     URL of the S3 bucket
    s3_index_file: A link to an index file in an s3 bucket.
    output_dor: Location where we're saving stuff locally

    """

    # open index file
    remote_index_handle = s3open( s3_url + "/" + s3_index_file )

    for site_name in remote_index_handle.readlines():

        site_name = site_name[:-1] # strip out newlines
        site_posts = site_name + "/Posts.xml"

        # make the output directory; if it exists simply continue
        try:
            os.makedirs( output_dir + "/" + site_name )
        except OSError:
            print( "Site directory '%s' exists locally, skipping." % site_name )
            continue

        # create pointers to the remote and local files
        remote_posts_handle = s3open( s3_url + "/" + site_posts )
        local_posts_handle = open( output_dir + "/" + site_posts, "w+" )

        for line in remote_posts_handle.readlines():
            local_posts_handle.write( line )

        local_posts_handle.close()
        remote_posts_handle.close()

    remote_index_handle.close()

# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    if len( sys.argv ) != 4:
        logging.error( "Usage: python pull_from_s3.py [s3_url]"
                       "[s3_index_file] [output_dir]" )
        sys.exit( 1 )

    s3_url = sys.argv[1]
    s3_index_file = sys.argv[2]
    output_dir = sys.argv[3]

    # pull in data from s3
    pull_from_s3( s3_url, s3_index_file, output_dir )

# }}}



