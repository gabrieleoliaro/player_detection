#!/usr/bin/python

import numpy as np
from covSEiso import *
from covNoise import *

def covSumCM(covfunc, loftheta, x):
    """
        covSum - compose a covariance function as the sum of other covariance
        functions. This function doesn't actually compute very much on its own, it
        merely does some bookkeeping, and calls other covariance functions to do the
        actual work.

        CM stands for Covariance Matrix

        For more help on design of covariance functions, try "help covFunctions".

        (C) Copyright 2006 by Carl Edward Rasmussen, 2006-03-20.
    """

    [n, D] = np.shape(x)

    # Pop the 'covSumCM' function out of the covfunc list, so that we use the array to compute the subcovariances
    if covfunc[0] == covSumCM:
        covfunc = covfunc[1:]

    # Create and fill j array with number of parameters for each covariance function to be used in the summation
    # Create and fill v array, which indicates to which covariance parameters belong
    j = np.array([])
    v = np.array([])
    for i in range(len(covfunc)):
        if (covfunc[i] is covSEisoCM) or (covfunc[i] is covSEisoTSC) or (covfunc[i] is covSEisoDERIV):
            j = np.append(j, 2)
        elif (covfunc[i] is covNoiseCM) or (covfunc[i] is covNoiseTSC) or (covfunc[i] is covNoiseDERIV):
            j = np.append(j, 1)
        else:
            j = np.append(j, "")

        v = np.concatenate((v, np.kron(np.ones((1, j[i])), i)))

 
    
    
    A = np.zeros((n, n))                  # Allocate space for covariance matrix
    for i in range(len(covfunc)):
        A = A + covfunc[i](logtheta * np.equal(v, i), x)

