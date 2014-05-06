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
def do_kmeans( data, labels, config ):
    """
    Do KMeans: perform KMeans clustering on an input corpus. Input is
    expected to be a dictionary of categories to tf-idf vectors.
    """

    init          = config.get("kmeans", "init")
    n_init     = config.getint("kmeans", "n_init")
    init_size  = config.getint("kmeans", "init_size")
    batch_size = config.getint("kmeans", "batch_size")

    km = cluster.MiniBatchKMeans(
        n_clusters=len(set(labels)), # expected number of clusters

        init=init,                   # initialization method (smart)
        n_init=n_init,               # number of random retries
        init_size=init_size,
        batch_size=batch_size
    )

    logging.info("Beginning KMeans clustering.")

    run_clustering( km, data, labels )
# }}}



# Perform Affinity Propagation {{{
def do_affinity_propagation( data, labels, config ):
    """
    Do Affinity Propagation: perform Affinity Propagation clustering on an
    input corpus.  Input is expected to be a dictionary of categories to
    tf-idf vectors.
    """

    damping        = config.getfloat("ap", "damping")
    convergence_iter = config.getint("ap", "convergence_iter")
    affinity            = config.get("ap", "affinity")

    ap = cluster.AffinityPropagation(
        damping=damping,                   # damping factor
        convergence_iter=convergence_iter, # convergence threshold
        affinity=affinity,                 # similarity metric
    )

    logging.info("Beginning Affinity Propagation clustering.")

    run_clustering( ap, data, labels )
# }}}



# Perform Mean Shift {{{
def do_mean_shift( data, labels, config ):
    """
    Do Mean Shift: perform Mean Shift clustering on an input corpus.  Input
    is expected to be a dictionary of categories to tf-idf vectors.
    """

    ms = cluster.MeanShift(
        min_bin_freq=1,     # only use bins with at least min frequency
        cluster_all=True,   # use all points
    )

    logging.info("Beginning Mean Shift clustering.")
    logging.warn("Meanshift is not a scalable clustering algorithm.")

    data = data.toarray()
    run_clustering( ms, data, labels )
# }}}



# Perform Spectral Clustering {{{
def do_spectral( data, labels, config ):
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
def do_wards( data, labels, config ):
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
def do_dbscan( data, labels, config ):
    """
    Do DBSCAN: perform DBSCAN clustering on an input corpus.
    Input is expected to be a dictionary of categories to tf-idf vectors.
    """

    eps       = config.getfloat("dbscan", "eps")
    min_samples = config.getint("dbscan", "min_samples")

    db = cluster.DBSCAN(
        eps=eps,                  # max distance between two neighbours
        min_samples=min_samples,  # number of neighbors for a core point
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
    algorithm_options = "kmeans|ap|meanshift|spectral|wards|dbscan"

    # ensure we have at least the minimum required params
    if len( sys.argv ) < 4:
        logging.error( "Usage: python cluster.py [input.ini] [cluster.ini] [%s]" %
                algorithm_options )
        sys.exit( 1 )

    # pull in parameters from the command line
    input_file  = sys.argv[1]
    config_file = sys.argv[2]
    requested_algorithms = sys.argv[3:]

    # read configuration file
    config = ConfigParser.ConfigParser( allow_no_value=True )
    config.readfp( open( input_file ) )
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
            do_kmeans( data, labels, config )

        if algorithm == "ap":
            do_affinity_propagation( data, labels, config )

        if algorithm == "meanshift":
            do_mean_shift( data, labels, config )

        if algorithm == "spectral":
            do_spectral( data, labels, config )

        if algorithm == "wards":
            do_wards( data, labels, config )

        if algorithm == "dbscan":
            do_dbscan( data, labels, config )
# }}}



