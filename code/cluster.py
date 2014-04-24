"""
Author: Michel Rouly
Date:   2014-04-24
"""


import sys
import logging

from sklearn import metrics
from sklearn.cluster import KMeans

from read_corpus import read_corpus



# Perform KMeans {{{
def do_kmeans( corpus ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning KMeans clustering.")

    return
# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    if len( sys.argv ) != 4:
        logging.error( "Usage: python cluster.py [s3|disk] data_dir [kmeans]" )
        sys.exit( 1 )

    # pull in parameters from the command line
    in_protocol = sys.argv[1]
    data_dir = sys.argv[2]
    algorithm = sys.argv[3]

    # available algorithms
    algorithms = ["kmeans",
                  "ap",
                  "meanshift",
                  "spectral",
                  "hierarchical",
                  "dbscan",
                  "gaussian"]

    # read and vectorize the corpus
    corpus = read_corpus( in_protocol=in_protocol, data_dir=data_dir )

    if algorithm == "kmeans":
        do_kmeans( corpus )

    if algorithm == "ap":
        do_ap( )

    if algorithm == "meanshift":
        do_meanshift( )
# }}}



