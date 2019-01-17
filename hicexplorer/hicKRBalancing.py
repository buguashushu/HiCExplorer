from KRBalancing import *
import numpy as np
import argparse

from hicmatrix import HiCMatrix as hm
from scipy import sparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""
Computes a balanced matrix using the Knight and Ruiz balancing algorithm.

    $ hicKRBalancing --matrix hic_matrix.h5 -o balanced_matrix.h5

"""
    )

    parserRequired = parser.add_argument_group('Required arguments')

    parserRequired.add_argument('--matrix', '-m',
                                help='HiCExplorer matrix in h5 format.',
                                required=True)

    parserRequired.add_argument('--outputFileName', '-o',
                                help='HiCExplorer matrix in h5 format.',
                                required=True)

    return parser


def main(args=None):
    args = parse_arguments().parse_args(args)
    ma = hm.hiCMatrix(args.matrix) #TODO slow for big matrices!
    ma.maskBins(ma.nan_bins)
    #TODO remove zero rows and columns
    print("float sparse matrix")
    d = kr_balancing(ma.matrix.astype(float))
    d.outter_loop()
    output = d.get_output()
    #print(np.array(output)) #TODO test sum of the rows and columns ! Plot the matrix! Assert the shape! PerChr!
    #print(np.sum(np.array(output), axis = 0))
    #print(np.sum(np.array(output), axis = 1))
    # assert all(i >= 0.9 for i in np.sum(np.array(output), axis = 0))
    # assert all(i <= 1.1 for i in np.sum(np.array(output), axis = 0))
    # assert all(i >= 0.9 for i in np.sum(np.array(output), axis = 1))
    # assert all(i <= 1.1 for i in np.sum(np.array(output), axis = 1))
    ma.setMatrixValues(np.array(output))
    ma.save(args.outputFileName, pApplyCorrection=False)

#if __name__ == "__main__":
#    main()
