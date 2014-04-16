from lxml import etree
import sys


if __name__ == "__main__":

    args = sys.argv
    num_args = len( sys.argv )

    if( num_args <= 1 ):
        print( "Usage: python strip_posts.py post_files" )
        exit( 1 )

    for arg in args[1:]:

        print( "Parsing %s" % arg )

        # construct tree over xml data
        tree = etree.parse( arg )
        rows = tree.iter("row")

        # for each row, split out its contents and output
        for row in rows:
            body = row.get("Body")
            print( body )

