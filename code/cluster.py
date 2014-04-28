"""
Author: Michel Rouly
Author: Joshua Wells
Date:   2014-04-28
"""

import sys
import logging
from time import time

from sklearn import metrics
from sklearn import cluster

from vectorize_data import vectorize_data



# Perform KMeans {{{
def do_kmeans( data, labels ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    # Construct a KMeans clustering machine
    km = cluster.MiniBatchKMeans(
        n_clusters=3,       # expected number of clusters
        init="k-means++",   # initialization method (smart)
        n_init=5,           # number of random retries
        #init_size=1000,
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
    logging.info("\tdone in       %fs"         % runtime)
    logging.info("\tHomogeneity:  %0.3f"       % homogeneity)
    logging.info("\tCompleteness: %0.3f"       % completeness)
    logging.info("\tV-measure:    %0.3f"       % v_measure)
    logging.info("\tAdjusted Rand-Index: %.3f" % adjusted_rand)
# }}}



# Perform Affinity Propagation {{{
def do_affinity_propagation( data, labels ):
    """
    Do Affinity Propagation: perform Affinity Propagation clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    # Construct an Affinity Propagation clustering machine
    ap = cluster.AffinityPropagation(
        damping=0.5,            # damping factor
        convergence_iter=15,    # number of no-change iterations to converge
        affinity="euclidean",   # similarity metric
    )

    logging.info("Beginning Affinity Propagation clustering.")

    t0 = time()
    ap.fit(data)
    t1 = time()

    # Perform metrics
    runtime       = (t1 - t0)
    homogeneity   = metrics.homogeneity_score(labels, ap.labels_)
    completeness  = metrics.completeness_score(labels, ap.labels_)
    v_measure     = metrics.v_measure_score(labels, ap.labels_)
    adjusted_rand = metrics.adjusted_rand_score(labels, ap.labels_)

    # Output
    logging.info("\tdone in       %fs"         % runtime)
    logging.info("\tHomogeneity:  %0.3f"       % homogeneity)
    logging.info("\tCompleteness: %0.3f"       % completeness)
    logging.info("\tV-measure:    %0.3f"       % v_measure)
    logging.info("\tAdjusted Rand-Index: %.3f" % adjusted_rand)
# }}}



# TODO: Perform Mean Shift {{{
def do_mean_shift( data, labels ):
    """
    Do Mean Shift: perform Mean Shift clustering on an input corpus.  Input
    is expected to be a dictionary of categories to tf-idf vectors.
    """

    # Construct a Mean Shift clustering machine
    ms = cluster.MeanShift(
        #bandwidth=,
        #seeds=,
        min_bin_freq=1,     # only use bins with at least min frequency
        cluster_all=True,   # use all points
    )

    logging.info("Beginning Mean Shift clustering.")
    logging.warn("Meanshift is not a scalable clustering algorithm.")

    data = data.toarray()
    t0 = time()
    ms.fit(data)
    t1 = time()

    # Perform metrics
    runtime       = (t1 - t0)
    homogeneity   = metrics.homogeneity_score(labels, ms.labels_)
    completeness  = metrics.completeness_score(labels, ms.labels_)
    v_measure     = metrics.v_measure_score(labels, ms.labels_)
    adjusted_rand = metrics.adjusted_rand_score(labels, ms.labels_)

    # Output
    logging.info("\tdone in       %fs"         % runtime)
    logging.info("\tHomogeneity:  %0.3f"       % homogeneity)
    logging.info("\tCompleteness: %0.3f"       % completeness)
    logging.info("\tV-measure:    %0.3f"       % v_measure)
    logging.info("\tAdjusted Rand-Index: %.3f" % adjusted_rand)
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



# Perform Ward's Hierarchical Clustering {{{
def do_wards( data, labels ):
    """
    Do Ward's Hierarchical: perform Ward's Hierarchical clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    # Construct a Ward's clustering machine
    ward = cluster.Ward(
        n_clusters=3,               # expected number of clusters
        connectivity=None,          # no connectivity matrix
    )

    logging.info("Beginning Ward's Hierarhical clustering.")

    data = data.toarray() # convert to a dense matrix
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
    logging.info("\tdone in       %fs"         % (t1 - t0))
    logging.info("\tHomogeneity:  %0.3f"       % homogeneity)
    logging.info("\tCompleteness: %0.3f"       % completeness)
    logging.info("\tV-measure:    %0.3f"       % v_measure)
    logging.info("\tAdjusted Rand-Index: %.3f" % adjusted_rand)
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

    if algorithm not in algorithms:
        logging.error( "Input \"%s\" is an unrecognized algorithm." % algorithm )
        sys.exit( 1 )

    # read and vectorize the data
    (labels, data) = vectorize_data( in_protocol=in_protocol,
                                     data_dir=data_dir )

    if algorithm == "kmeans":
        do_kmeans( data, labels )

    if algorithm == "ap":
        do_affinity_propagation( data, labels )

    if algorithm == "meanshift":
        do_mean_shift( data, labels )

    if algorithm == "spectral":
        do_spectral( data, labels )

    if algorithm == "wards":
        do_wards( data, labels )

    if algorithm == "dbscan":
        do_dbscan( data, labels )

    if algorithm == "gaussian":
        do_gaussian( data)
# }}}



