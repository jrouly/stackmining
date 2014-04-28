"""
Author: Michel Rouly
Date:   2014-04-24
"""

import sys
import logging
from time import time

from sklearn import metrics

from sklearn.cluster import KMeans          # KMeans
from sklearn.cluster import Ward            # Ward's method
from sklearn.cluster import MiniBatchKMeans # Mini batch KMeans

from vectorize_data import vectorize_data



# TODO: Perform KMeans {{{
def do_kmeans( data, labels ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    # Construct a KMeans clustering machine
    km = MiniBatchKMeans(
        n_clusters=8,
        init='k-means++',
        n_init=1,
        init_size=1000,
        batch_size=1000
    )

    logging.info("Beginning KMeans clustering.")

    t0 = time()
    km.fit(data)
    t1 = time()

    # Perform metrics
    runtime       = (t1 - t0)
    homogeneity   = metrics.homogeneity_score(labels, km.labels_)
    completeness  = metrics.completeness_score(labels, km.labels_)
    v_measure     = metrics.v_measure_score(labels, km.labels_)
    adjusted_rand = metrics.adjusted_rand_score(labels, km.labels_)

    # Output
    logging.info("done in       %fs"         % runtime)
    logging.info("Homogeneity:  %0.3f"       % homogeneity)
    logging.info("Completeness: %0.3f"       % completeness)
    logging.info("V-measure:    %0.3f"       % v_measure)
    logging.info("Adjusted Rand-Index: %.3f" % adjusted_rand)
# }}}



# TODO: Perform Affinity Propagation {{{
def do_affinity_propagation( data, labels ):
    """
    Do Affinity Propagation: perform Affinity Propagation clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    logging.info("Beginning Affinity Propagation clustering.")

    return
# }}}



# TODO: Perform Mean Shift {{{
def do_mean_shift( data, labels ):
    """
    Do Mean Shift: perform Mean Shift clustering on an input corpus.  Input
    is expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning Mean Shift clustering.")

    return
# }}}



# TODO: Perform Spectral Clustering {{{
def do_spectral( data, labels ):
    """
    Do Spectral: perform Spectral clustering on an input corpus.  Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning Spectral clustering.")

    return
# }}}



# TODO: Perform Ward's Hierarchical Clustering {{{
def do_wards( data, labels ):
    """
    Do Ward's Hierarchical: perform Ward's Hierarchical clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    # Construct a Ward's clustering machine
    ward = Ward(
        n_clusters=2,
        connectivity=None,
        n_components=None,
        compute_full_tree='auto'
    )

    logging.info("Beginning Ward's Hierarhical clustering.")

    data = data.toarray()
    t0 = time()
    ward.fit(data)
    t1 = time()

    # Perform metrics
    runtime       = (t1 - t0)
    homogeneity   = metrics.homogeneity_score(labels, ward.labels_)
    completeness  = metrics.completeness_score(labels, ward.labels_)
    v_measure     = metrics.v_measure_score(labels, ward.labels_)
    adjusted_rand = metrics.adjusted_rand_score(labels, ward.labels_)

    # Output
    logging.info("done in       %fs"         % (t1 - t0))
    logging.info("Homogeneity:  %0.3f"       % homogeneity)
    logging.info("Completeness: %0.3f"       % completeness)
    logging.info("V-measure:    %0.3f"       % v_measure)
    logging.info("Adjusted Rand-Index: %.3f" % adjusted_rand)
# }}}



# TODO: Perform DBSCAN {{{
def do_dbscan( data, labels ):
    """
    Do DBSCAN: perform DBSCAN clustering on an input corpus.
    Input is expected to be a dictionary of categories to tf-idf vectors.
    """

    logging.info("Beginning DBSCAN clustering.")

    return
# }}}



# TODO: Perform Gaussian {{{
def do_gaussian( data, labels ):
    """
    Do Gaussian: perform Gaussian Mixture Modeling clustering on an input
    corpus.  Input is expected to be a dictionary of categories to tf-idf
    vectors.
    """

    logging.info("Beginning Gaussian Mixture Modeling clustering.")

    return
# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    algorithms = "kmeans|ap|meanshift|spectral|wards|dbscan|gaussian"

    if len( sys.argv ) != 4:
        logging.error( "Usage: python cluster.py [s3|disk] data_dir [%s]" %
                algorithms )
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
                  "wards",
                  "dbscan",
                  "gaussian"]

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

    if algorithm == "wards":
        do_wards( data, labels )

    if algorithm == "dbscan":
        do_dbscan( data, labels )

    if algorithm == "gaussian":
        do_gaussian( data)
# }}}



