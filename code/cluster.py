"""
Author: Michel Rouly
Date:   2014-04-24
"""


import sys
import logging

from sklearn import metrics
from sklearn.cluster import KMeans

from vectorize_data import vectorize_data



# Perform KMeans {{{
def do_kmeans( data, labels ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning KMeans clustering.")
    km = KMeans(n_clusters=8, init='k-means++', max_iter=100, n_init=1)

    km.fit(data)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
    print("Adjusted Rand-Index: %.3f"
      % metrics.adjusted_rand_score(labels, km.labels_))
    return
# }}}



# Perform Affinity Propagation {{{
def do_affinity_propagation( data, labels ):
    """
    Do Affinity Propagation: perform Affinity Propagation clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    logging.info("Beginning Affinity Propagation clustering.")

    return
# }}}



# Perform Mean Shift {{{
def do_mean_shift( data, labels ):
    """
    Do Mean Shift: perform Mean Shift clustering on an input corpus.  Input
    is expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning Mean Shift clustering.")

    return
# }}}



# Perform Spectral Clustering {{{
def do_spectral( data, labels ):
    """
    Do Spectral: perform Spectral clustering on an input corpus.  Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning Spectral clustering.")

    return
# }}}



# Perform Hierarchical {{{
def do_hierarchical( data, labels ):
    """
    Do Hierarchical: perform Hierarchical clustering on an input corpus.
    Input is expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning Hierarhical clustering.")

    return
# }}}



# Perform DBSCAN {{{
def do_dbscan( data, labels ):
    """
    Do DBSCAN: perform DBSCAN clustering on an input corpus.
    Input is expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning DBSCAN clustering.")

    return
# }}}



# Perform Gaussian {{{
def do_gaussian( data, labels ):
    """
    Do Gaussian: perform Gaussian Mixture Modeling clustering on an input
    corpus.  Input is expected to be a dictionary of categories to tf-idf
    vectors.
    """

    logging.info("Beginning Gaussian Mixture Modeling clustering.")

    return
# }}}



# Debug method {{{
def do_debug( data, labels ):
    """
    Do Debug: Just for testing and funsies.
    """

    logging.info("Beginning debug clustering.")

    #from sklearn.naive_bayes import GaussianNB
    #clf = GaussianNB()
    #clf.fit( data.toarray()[:-5], labels[:-5] )
    #predictions = clf.predict( data.toarray()[-5:] )

    #logging.debug( predictions )
    #logging.debug( labels[-5:] )

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
                  "gaussian",
                  "debug"]

    # read and vectorize the data
    (labels, data) = vectorize_data( in_protocol=in_protocol,
                                     data_dir=data_dir )

    if algorithm == "kmeans":
        do_kmeans( data, labels )

    if algorithm == "ap":
        do_ap( data, labels )

    if algorithm == "meanshift":
        do_meanshift( data, labels )

    if algorithm == "spectral":
        do_spectral( data, labels )

    if algorithm == "hierarhical":
        do_hierarchical( data, labels )

    if algorithm == "dbscan":
        do_dbscan( data, labels )

    if algorithm == "gaussian":
        do_gaussian( data)

    if algorithm == "debug":
        do_debug( data, labels )
# }}}



