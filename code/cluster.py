"""
Author: Michel Rouly
Author: Joshua Wells
Date:   2014-04-28
"""

import sys
import logging
import ConfigParser
from time import time

from sklearn import metrics
from sklearn import cluster

from vectorize_data import vectorize_data



# Run clustering algorithm {{{
def run_clustering( clusterer, data, labels ):
    """
    Cluster: Using a predefined and parameterized clustering algorithm, fit
    some dataset and perform metrics given a set of ground-truth labels.

        clusterer: the clustering algorithm, from sklearn
        data:      array-like dataset input
        labels:    vector of ground-truth labels

    """

    # Time the operation
    t0 = time()
    clusterer.fit(data)
    t1 = time()

    # Perform metrics
    runtime         = (t1 - t0)
    homogeneity     = metrics.homogeneity_score(   labels, clusterer.labels_ )
    completeness    = metrics.completeness_score(  labels, clusterer.labels_ )
    v_measure       = metrics.v_measure_score(     labels, clusterer.labels_ )
    adjusted_rand   = metrics.adjusted_rand_score( labels, clusterer.labels_ )
    adjusted_mutual = metrics.adjusted_mutual_info_score( labels,
                                                          clusterer.labels_ )

    # Output to logs
    logging.info("  |-        Execution time: %fs"   % runtime)
    logging.info("  |-           Homogeneity: %0.3f" % homogeneity)
    logging.info("  |-          Completeness: %0.3f" % completeness)
    logging.info("  |-             V-measure: %0.3f" % v_measure)
    logging.info("  |-   Adjusted Rand-Index: %.3f"  % adjusted_rand)
    logging.info("  |-  Adjusted Mutual Info: %.3f"  % adjusted_mutual)
# }}}



# Perform KMeans {{{
def do_kmeans( data, labels ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    km = cluster.MiniBatchKMeans(
        n_clusters=len(set(labels)), # expected number of clusters
        init="k-means++",            # initialization method (smart)
        n_init=5,                    # number of random retries
        #init_size=1000,
        batch_size=1000
    )

    logging.info("Beginning KMeans clustering.")

    run_clustering( km, data, labels )
# }}}



# Perform Affinity Propagation {{{
def do_affinity_propagation( data, labels ):
    """
    Do Affinity Propagation: perform Affinity Propagation clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    ap = cluster.AffinityPropagation(
        damping=0.5,            # damping factor
        convergence_iter=15,    # number of no-change iterations to converge
        affinity="euclidean",   # similarity metric
    )

    logging.info("Beginning Affinity Propagation clustering.")

    run_clustering( ap, data, labels )
# }}}



# Perform Mean Shift {{{
def do_mean_shift( data, labels ):
    """
    Do Mean Shift: perform Mean Shift clustering on an input corpus.  Input
    is expected to be a dictionary of categories to tf-idf vectors.
    """

    ms = cluster.MeanShift(
        #bandwidth=,
        #seeds=,
        min_bin_freq=1,     # only use bins with at least min frequency
        cluster_all=True,   # use all points
    )

    logging.info("Beginning Mean Shift clustering.")
    logging.warn("Meanshift is not a scalable clustering algorithm.")

    data = data.toarray()
    run_clustering( ms, data, labels )
# }}}



# Perform Spectral Clustering {{{
def do_spectral( data, labels ):
    """
    Do Spectral: perform Spectral clustering on an input corpus.  Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    sc = cluster.SpectralClustering(
        n_clusters=len(set(labels)), # expected number of clusters
        eigen_solver="arpack",       # eigenvalue decomposition strategy
        assign_labels="discretize",  # label assignment strategy
    )

    logging.info("Beginning Spectral clustering.")

    run_clustering( sc, data, labels )
# }}}



# Perform Ward's Hierarchical Clustering {{{
def do_wards( data, labels ):
    """
    Do Ward's Hierarchical: perform Ward's Hierarchical clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    wh = cluster.Ward(
        n_clusters=len(set(labels)), # expected number of clusters
        connectivity=None,           # no connectivity matrix
    )

    logging.info("Beginning Ward's Hierarhical clustering.")

    data = data.toarray()
    run_clustering( wh, data, labels )
# }}}



# Perform DBSCAN {{{
def do_dbscan( data, labels ):
    """
    Do DBSCAN: perform DBSCAN clustering on an input corpus.
    Input is expected to be a dictionary of categories to tf-idf vectors.
    """

    db = cluster.DBSCAN(
        eps=0.01,          # max distance between two neighbours
        min_samples=1,  # number of neighbors for a core point
        #metric=,       #
        #random_state=, #
    )

    logging.info("Beginning DBSCAN clustering.")

    data = data.toarray()
    run_clustering( db, data, labels )
# }}}



# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    # algorithm options
    options = "kmeans|ap|meanshift|spectral|wards|dbscan"

    # ensure we have at least the minimum required params
    if len( sys.argv ) < 3:
        logging.error( "Usage: python cluster.py [config.ini] [%s]" %
                options )
        sys.exit( 1 )

    # pull in parameters from the command line
    config_file = sys.argv[1]
    requested_algorithms = sys.argv[2:]

    # read configuration file
    config = ConfigParser.ConfigParser( allow_no_value=True )
    config.readfp( open( config_file ) )

    # available algorithms
    known_algorithms = ["kmeans",
                        "ap",
                        "meanshift",
                        "spectral",
                        "wards",
                        "dbscan"]

    # read and vectorize the data
    (labels, data) = vectorize_data( config )

    # loop over all requested algorithms
    for algorithm in requested_algorithms:

        # verify that requested algorithm is known
        if algorithm not in known_algorithms:
            logging.error( "Algorithm \"%s\" is not recognized." % algorithm )

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
# }}}



