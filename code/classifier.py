"""
Author: Michel Rouly
Author: Joshua Wells
Date:   2014-05-07
Desc:   Perform a classification procedure on the input data set and output
        formatted metrics.
"""

import sys
import logging
import ConfigParser
from time import time

from sklearn import metrics
from sklearn import tree
from sklearn import cross_validation
from sklearn import naive_bayes
from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble

from vectorize_data import vectorize_data



# Run clustering algorithm {{{
def run_classification( classifier, data, labels ):

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        data,
        labels,
        test_size=0.4,
        random_state=0
    )

    # Time the operation
    t0 = time()
    classifier.fit(X_train, y_train)
    t1 = time()

    y_predict = classifier.predict(X_test)

    # Perform metrics
    runtime               = (t1 - t0)
    accuracy              = metrics.accuracy_score(y_test, y_predict)
    classification_report = metrics.classification_report(y_test, y_predict)
    confusion_matrix      = metrics.confusion_matrix(y_test, y_predict)

    # Output to logs
    logging.info("  |-        Execution time: %fs"   % runtime)
    logging.info("  |-              Accuracy: %0.3f" % accuracy)
    logging.info("  |-          Confusion Matrix:\n" + str (confusion_matrix))
    logging.info("\n|-             Classification Report:\n" + str(classification_report))
# }}}



# Perform DTree {{{
def do_dtree( data, labels, config ):

    max_depth = config.getint("dtree", "max_depth")

    dt = tree.DecisionTreeClassifier(
    )

    logging.info("Beginning Decision Tree classification.")
    data = data.toarray()
    run_classification( dt, data, labels )
# }}}

# Perform RandomForest {{{
def do_randomForest( data, labels, config ):

    max_depth = config.getint("dtree", "max_depth")

    rf = ensemble.RandomForestClassifier()

    logging.info("Beginning Random Forest classification.")
    data = data.toarray()
    run_classification( rf, data, labels )
# }}}

# Perform naiveBayes {{{
def do_naiveBayes( data, labels, config ):

    nb = naive_bayes.GaussianNB()

    logging.info("Beginning NaiveBayes classification.")
    data = data.toarray()
    run_classification( nb, data, labels )
# }}}

# Perform k-nearest neighbor {{{
def do_kNeighbor( data, labels, config ):

    #Possible useful args:
    #n_neighbor=int
    #weights='uniform'|'distance'
    kn = neighbors.KNeighborsClassifier()

    logging.info("Beginning K-Nearest Neighbor classification.")
    data = data.toarray()
    run_classification( kn, data, labels )
# }}}

# Perform svm {{{
def do_svm( data, labels, config ):

    #Possible useful args:
    #class_weight: {dict}
    #C
    #http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC
    sv = svm.LinearSVC()

    logging.info("Beginning SVM classification.")
    data = data.toarray()
    run_classification( sv, data, labels )
# }}}


# Executable (Main) {{{
if __name__ == "__main__":

    # turn on logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')

    # algorithm options
    algorithm_options = "dtree|randomforest|nbayes|kNeighbor|svm"

    # ensure we have at least the minimum required params
    if len( sys.argv ) < 4:
        logging.error( "Usage: python classifier.py [input.ini] [classifier.ini] [%s]" %
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
    known_algorithms = ["dtree","randomforest","nbayes","kNeighbor","svm"]

    # read and vectorize the data
    (labels, data) = vectorize_data( config )

    # loop over all requested algorithms
    for algorithm in requested_algorithms:

        # verify that requested algorithm is known
        if algorithm not in known_algorithms:
            logging.error( "Algorithm \"%s\" is not recognized." % algorithm )

        if algorithm == "dtree":
            do_dtree( data, labels, config )

        if algorithm == "randomforest":
            do_randomForest( data, labels, config )

        if algorithm == "nbayes":
            do_naiveBayes( data, labels, config )

        if algorithm == "kNeighbor":
            do_kNeighbor( data, labels, config )

        if algorithm == "svm":
            do_svm( data, labels, config )




# }}}
