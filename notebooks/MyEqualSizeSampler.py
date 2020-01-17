# This script is part of the supporting information to the manuscript entitled "KnowTox: Pipeline and Case Study for Confident
# Prediction of Potential Toxic Effects of Compounds in Early Phases of Development". The script was developed by Andrea Morger 
# in the In Silico Toxicology and Structural Biology Group of Prof. Dr. Andrea Volkamer at the Charité Universitätsmedizin 
# Berlin, in collaboration with BASF SE in Ludwigshafen. It was last updated in January 2020.

import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold
            
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold
     

class EqualSizeSampler(object):
    """Equal size sampler.
    
    This class was adapted from the RandomSubSampler class of the nonconformist package by Henrik Linusson
    https://github.com/donlnz/nonconformist
    
    Equal size sampling is not necessary for typical conformal predictors with mondrian condition. In the special case of 
    fitting an additional normaliser model, the equal size sampling could clearly improve the efficiency as well as the 
    balance of the evaluation parameters between the active and inactive class.
    
    Thus, a new class called EqualSizeSampler is provided here that allows subsampling of proper training and calibration sets to
    the same number of active and inactive compounds.  
    
    This class was updated to be compatible with scikit-learn version 0.22.1.
   
    """

    def __init__(self, calibration_portion=0.3):
        self.cal_portion = calibration_portion

    def gen_samples(self, X, y, n_samples, problem_type, ratio=1):
        
        # Split training data into calibration and proper training set
        splits = StratifiedShuffleSplit(n_splits=5,
                                        test_size=self.cal_portion).split(X,y)
        for train, cal in splits:
            y_train = y[train]
            
            # Mask to distinguish compounds of inactive and active class of proper training set
            mask_0 = y_train == 0
            train_0 = train[mask_0]
            mask_1 = y_train == 1
            train_1 = train[mask_1]
            
            # Define which class corresponds to larger proper training set and is subject to undersampling
            larger = (train_0 if train_0.size > train_1.size else train_1)
            smaller = (train_1 if train_0.size > train_1.size else train_0)

            # Subsampling of larger class until same number of instances as for smaller class is reached
            while smaller.size < larger.size/ratio:
                k = np.random.choice(range(larger.size))
                larger = np.delete(larger, k)

            train = sorted(np.append(larger, smaller))

            # Mask to distinguish compounds of inactive and active class of calibration set
            y_cal = y[cal]
            mask_c_0 = y_cal == 0
            cal_0 = cal[mask_c_0]
            mask_c_1 = y_cal == 1
            cal_1 = cal[mask_c_1]

            # Define which class corresponds to larger calibration set and is subject to undersampling
            larger_c = (cal_0 if cal_0.size > cal_1.size else cal_1)
            smaller_c = (cal_1 if cal_0.size > cal_1.size else cal_0)

            # Subsampling of larger class until same number of instances as for smaller class is reached
            while smaller_c.size < larger_c.size / ratio:
                k = np.random.choice(range(larger_c.size))
                larger_c = np.delete(larger_c, k)

            cal = sorted(np.append(larger_c, smaller_c))
            
            # Return equal size sampled proper training and calibration set
            yield train, cal